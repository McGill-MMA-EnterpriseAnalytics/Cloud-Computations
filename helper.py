#import libraries
import pandas as pd
import requests
from io import StringIO
import ssl
import json
from pprint import pprint
import requests
import os
from pandas import json_normalize 
from sklearn.experimental import enable_iterative_imputer
from sklearn.impute import IterativeImputer
from datetime import datetime
    
ssl._create_default_https_context = ssl._create_unverified_context
def load_csv(url):
    #orig_url=url
    file_id = url#'https://drive.google.com/uc?export=download&id='+orig_url.split('/')[-2]
    dfs = pd.read_csv(file_id,error_bad_lines=False)
    return(dfs)

def load_data(cityname="Montreal"):
    city_url="https://enterprisemcgill.s3.amazonaws.com/city_attributes.csv"
    city=load_csv(city_url)
    weather_desc_url="https://enterprisemcgill.s3.amazonaws.com/weather_description.csv"
    weather_desc=load_csv(weather_desc_url)
    humidity_url="https://enterprisemcgill.s3.amazonaws.com/humidity.csv"
    humidity=load_csv(humidity_url)
    pressure_url="https://enterprisemcgill.s3.amazonaws.com/pressure.csv"
    pressure=load_csv(pressure_url)
    temp_url="https://enterprisemcgill.s3.amazonaws.com/temp.csv"
    temp=load_csv(temp_url)
    wind_direction_url="https://enterprisemcgill.s3.amazonaws.com/wind_direction.csv"
    wind_direction=load_csv(wind_direction_url)
    wind_speed_url="https://enterprisemcgill.s3.amazonaws.com/wind_speed.csv"
    wind_speed=load_csv(wind_speed_url)
    
    city.columns="city"+city.columns
    weather_desc.columns="weather"+weather_desc.columns
    humidity.columns="humidity"+humidity.columns
    pressure.columns="pressure"+pressure.columns
    temp.columns="temp"+temp.columns
    wind_direction.columns="wind_direction"+wind_direction.columns
    wind_speed.columns="wind_speed"+wind_speed.columns
    data=pd.concat([city,weather_desc,humidity,pressure,temp,wind_direction,wind_speed],axis=1)
    allcitydata=data[data.columns[data.columns.str.contains(cityname+"|weatherdate")]]
    allcitydata.columns= ['datetime','Description','Humidity','Wind Direction','Temperature','Pressure','Wind Speed']

    #allcitydata = allcitydata.drop("city",axis=1)
    return(city,weather_desc,humidity,pressure,temp,wind_direction,wind_speed,allcitydata)


def api(city):
    API_KEY=os.getenv('WEATHER_API')
    r = requests.get('http://api.openweathermap.org/data/2.5/weather?q="+city+"&APPID=484925ef3995e2026aa4d24818ac18b1')


    response=json.loads(r.text)
    response_cols=response.keys()
    data=json_normalize(json.loads(r.text))
    weather=json_normalize(json.loads(r.text),record_path=['weather'])
    weather.columns='weather.'+weather.columns
    final_data=pd.concat([data[data.columns[1:len(data.columns)]],weather],axis=1)
    return(final_data)

def load_and_preprocess(cityname="Montreal"):
    city,weather_desc,humidity,pressure,temp,wind_direction,wind_speed,montreal = load_data(cityname=cityname)
    montreal=impute(montreal)
    montreal=clean_description(montreal)
    return(montreal)

##########NEW##########
#takes the montreal df as input and imputes the columns
def impute(df):
  df = df.drop(0) #dropping first row of nulls

  for col in list(df.drop(['datetime', 'Description'], axis = 1).columns): #run iterative imputer on each column
    imp = IterativeImputer(random_state = 6)
    df[[col]] = imp.fit_transform(df[[col]])

  return df

#NEW - preprocessing for the description weather column - from Steven
def clean_description(df):
    #too much detail, simplifying a bit and cleaning/standarizing word notation
    df['Description'] = df['Description'].str.replace(' with ', ' ')
    df['Description'] = df['Description'].str.replace(' and ', ' ')
    df['Description'] = df['Description'].str.replace('proximity ', '')
    df['Description'] = df['Description'].str.replace('light intensity', 'light')
    df['Description'] = df['Description'].str.replace('heavy intensity', 'heavy')
    df['Description'] = df['Description'].str.replace('very heavy', 'heavy')

    #exceptions / categories that the same
    df['Description'] = df['Description'].str.replace('light drizzle rain', 'light rain')
    df['Description'] = df['Description'].str.replace('light drizzle', 'light rain')
    df['Description'] = df['Description'].str.replace('drizzle', 'light rain')
    df['Description'] = df['Description'].str.replace('sleet', 'snow')
    df['Description'] = df['Description'].str.replace('freezing', 'snow')
    df['Description'] = df['Description'].str.replace('sand', 'other')
    df['Description'] = df['Description'].str.replace('dust', 'other')
    df['Description'] = df['Description'].str.replace('smoke', 'other')

    #standarizing intensity values
    df['Description'] = df['Description'].str.replace('few', 'light ')
    df['Description'] = df['Description'].str.replace('broken', 'moderate ')
    df['Description'] = df['Description'].str.replace('scattered', 'moderate ')
    df['Description'] = df['Description'].str.replace('overcast ', 'heavy ')
    
    #multi-categorical dummification
    tags = ['clouds','rain','mist','snow','shower','thunderstorm','fog','other']

    for i in range(len(tags)):
        df[tags[i]]=0
        df.loc[df['Description'].str.contains(pat=tags[i])==True, tags[i]] = 1
        
    #creating a weather intensity column
    intensity_values=['sky is clear','light','moderate','heavy']    

    for i in range(len(intensity_values)):
        df.loc[df['Description'].str.contains(pat =intensity_values[i])==True, 'Intensity'] = i


    #fill in the blanks with moderate
    df['Intensity']=df['Intensity'].fillna(2)
    
    return df

def feature_engineer(df): #implementing Hanna's features in a function
    df['datetime'] = pd.to_datetime(df['datetime'])
    df['year'] = df['datetime'].dt.year
    df['month'] = df['datetime'].dt.month
    df['day'] = df['datetime'].dt.day
    df['hour'] = df['datetime'].dt.hour
    df['minute'] = df['datetime'].dt.minute
    df['weekday'] = df['datetime'].dt.weekday
    df['week'] = df['datetime'].dt.weekofyear
    df['quarter'] = df['datetime'].dt.quarter
    df['month start'] = df['datetime'].dt.is_month_start
    df['month end'] = df['datetime'].dt.is_month_end
    df['quarter start'] = df['datetime'].dt.is_quarter_start
    df['quarter end'] = df['datetime'].dt.is_quarter_end

    df = df.set_index('datetime')
    df['max daily temp']=df.resample('D')['Temperature'].transform('max')
    df['max daily temp']=df['max daily temp'].shift(24)
    df['max daily hum']=df.resample('D')['Humidity'].transform('max')
    df['max daily hum']=df['max daily hum'].shift(24)
    df['max daily wind speed']=df.resample('D')['Wind Speed'].transform('max')
    df['max daily wind speed']=df['max daily wind speed'].shift(24)
    df['max daily wind direction']=df.resample('D')['Wind Direction'].transform('max')
    df['max daily wind direction']=df['max daily wind direction'].shift(24)
    df['max daily pressure']=df.resample('D')['Pressure'].transform('max')
    df['max daily pressure']=df['max daily pressure'].shift(24)

    df['max weekly temp']=df.resample('W')['Temperature'].transform('max')
    df['max weekly temp']=df['max weekly temp'].shift(168)
    df['max weekly hum']=df.resample('W')['Humidity'].transform('max')
    df['max weekly hum']=df['max weekly hum'].shift(168)
    df['max weekly wind speed']=df.resample('W')['Wind Speed'].transform('max')
    df['max weekly wind speed']=df['max weekly wind speed'].shift(168)
    df['max weekly wind direction']=df.resample('W')['Wind Direction'].transform('max')
    df['max weekly wind direction']=df['max weekly wind direction'].shift(168)
    df['max weekly pressure']=df.resample('W')['Pressure'].transform('max')
    df['max weekly pressure']=df['max weekly pressure'].shift(168)

    df['min daily temp']=df.resample('D')['Temperature'].transform('min')
    df['min daily temp']=df['min daily temp'].shift(24)
    df['min daily hum']=df.resample('D')['Humidity'].transform('min')
    df['min daily hum']=df['min daily temp'].shift(24)
    df['min daily wind speed']=df.resample('D')['Wind Speed'].transform('min')
    df['min daily wind speed']=df['min daily temp'].shift(24)
    df['min daily wind direction']=df.resample('D')['Wind Direction'].transform('min')
    df['min daily wind direction']=df['min daily temp'].shift(24)
    df['min daily pressure']=df.resample('D')['Pressure'].transform('min')
    df['min daily pressure']=df['min daily temp'].shift(24)


    df['min weekly temp']=df.resample('W')['Temperature'].transform('min')
    df['min weekly temp']=df['min weekly temp'].shift(168)
    df['min weekly hum']=df.resample('W')['Humidity'].transform('min')
    df['min weekly hum']=df['min weekly hum'].shift(168)
    df['min weekly wind speed']=df.resample('W')['Wind Speed'].transform('min')
    df['min weekly wind speed']=df['min weekly wind speed'].shift(168)
    df['min weekly wind direction']=df.resample('W')['Wind Direction'].transform('min')
    df['min weekly wind direction']=df['min weekly wind direction'].shift(168)
    df['min weekly pressure']=df.resample('W')['Pressure'].transform('min')
    df['min weekly pressure']=df['min weekly pressure'].shift(168)

    df['mean daily temp']=df.resample('D')['Temperature'].transform('max')
    df['mean daily temp']=df['mean daily temp'].shift(24)
    df['mean daily hum']=df.resample('D')['Humidity'].transform('max')
    df['mean daily hum']=df['mean daily hum'].shift(24)
    df['mean daily wind speed']=df.resample('D')['Wind Speed'].transform('max')
    df['mean daily wind speed']=df['mean daily wind speed'].shift(24)
    df['mean daily wind direction']=df.resample('D')['Wind Direction'].transform('max')
    df['mean daily wind direction']=df['mean daily wind direction'].shift(24)
    df['mean daily pressure']=df.resample('D')['Pressure'].transform('max')
    df['mean daily pressure']=df['mean daily pressure'].shift(24)

    df['mean weekly temp']=df.resample('W')['Temperature'].transform('mean')
    df['mean weekly temp']=df['mean weekly temp'].shift(168)
    df['mean weekly hum']=df.resample('W')['Humidity'].transform('mean')
    df['mean weekly hum']=df['mean weekly hum'].shift(168)
    df['mean weekly wind speed']=df.resample('W')['Wind Speed'].transform('mean')
    df['mean weekly wind speed']=df['mean weekly wind speed'].shift(168)
    df['mean weekly wind direction']=df.resample('W')['Wind Direction'].transform('mean')
    df['mean weekly wind direction']=df['mean weekly wind direction'].shift(168)
    df['mean weekly pressure']=df.resample('W')['Pressure'].transform('mean')
    df['mean weekly pressure']=df['mean weekly pressure'].shift(168)

    df['rolling_mean_temp'] = df['Temperature'].rolling(window=24).mean()
    df['rolling_mean_pressure'] = df['Pressure'].rolling(window=24).mean()
    df['rolling_mean_wind_dir'] = df['Wind Direction'].rolling(window=24).mean()
    df['rolling_mean_wind_speed'] = df['Wind Speed'].rolling(window=24).mean()
    df['rolling_mean_humidity'] = df['Humidity'].rolling(window=24).mean()

    df['rolling_min_temp'] = df['Temperature'].rolling(window=24).min()
    df['rolling_min_pressure'] = df['Pressure'].rolling(window=24).min()
    df['rolling_min_wind_dir'] = df['Wind Direction'].rolling(window=24).min()
    df['rolling_min_wind_speed'] = df['Wind Speed'].rolling(window=24).min()
    df['rolling_min_humidity'] = df['Humidity'].rolling(window=24).min()

    df['rolling_max_temp'] = df['Temperature'].rolling(window=24).max()
    df['rolling_max_pressure'] = df['Pressure'].rolling(window=24).max()
    df['rolling_max_wind_dir'] = df['Wind Direction'].rolling(window=24).max()
    df['rolling_max_wind_speed'] = df['Wind Speed'].rolling(window=24).max()
    df['rolling_max_humidity'] = df['Humidity'].rolling(window=24).max()

    df['rolling_mean_temp'] = df['Temperature'].expanding(2).mean()
    df['rolling_mean_pressure'] = df['Pressure'].expanding(2).mean()
    df['rolling_mean_wind_dir'] = df['Wind Direction'].expanding(2).mean()
    df['rolling_mean_wind_speed'] = df['Wind Speed'].expanding(2).mean()
    df['rolling_mean_humidity'] = df['Humidity'].expanding(2).mean()

    df['rolling_min_temp'] = df['Temperature'].expanding(2).min()
    df['rolling_min_pressure'] = df['Pressure'].expanding(2).min()
    df['rolling_min_wind_dir'] = df['Wind Direction'].expanding(2).min()
    df['rolling_min_wind_speed'] = df['Wind Speed'].expanding(2).min()
    df['rolling_min_humidity'] = df['Humidity'].expanding(2).min()

    df['rolling_max_temp'] = df['Temperature'].expanding(2).max()
    df['rolling_max_pressure'] = df['Pressure'].expanding(2).max()
    df['rolling_max_wind_dir'] = df['Wind Direction'].expanding(2).max()
    df['rolling_max_wind_speed'] = df['Wind Speed'].expanding(2).max()
    df['rolling_max_humidity'] = df['Humidity'].expanding(2).max()
    
    return(df)

def feature_engineer_important(df):
    df = feature_engineer(df) #create new features using above
    
    important_features = ['Humidity', 
                          'Wind Direction', 
                          'Pressure',
                          'hour',
                          'week',
                          'max daily temp',
                          'min daily temp',
                          'min daily hum', 
                          'min weekly temp',
                          'mean daily temp', 
                          'mean daily pressure', 
                          'mean weekly temp', 
                          'rolling_mean_temp', 
                          'rolling_mean_pressure', 
                          'rolling_mean_wind_speed', 
                          'Temperature']
    df = df[important_features] #only return the top 15 most important features
    
    return(df)
