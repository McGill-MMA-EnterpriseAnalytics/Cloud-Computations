import pandas as pd
import requests
from io import StringIO
import ssl
from pandas_profiling import ProfileReport
import streamlit as st
import streamlit.components.v1 as components
import plotly.express as px
import plotly.figure_factory as ff
import json
from pprint import pprint
import requests
import os
from pandas import json_normalize 
    
ssl._create_default_https_context = ssl._create_unverified_context
def load_csv(url):
    orig_url=url
    file_id = 'https://drive.google.com/uc?export=download&id='+orig_url.split('/')[-2]
    dfs = pd.read_csv(file_id,error_bad_lines=False)
    return(dfs)

def load_data():
    city_url="https://drive.google.com/file/d/1zYkIQtKO34UEILfNeIpPCnfIwCtZcmzD/view?usp=sharing"
    city=load_csv(city_url)
    weather_desc_url="https://drive.google.com/file/d/1-9uMFJnLZSJLdyZeST6G2AArtR--yMJa/view?usp=sharing"
    weather_desc=load_csv(weather_desc_url)
    humidity_url="https://drive.google.com/file/d/1-38LryQSt16wh4JXteC049sHWYqoyc3d/view?usp=sharing"
    humidity=load_csv(humidity_url)
    pressure_url="https://drive.google.com/file/d/1-1ZCUKvf6LE7BBQnchnBk4U5Q0qO58IY/view?usp=sharing"
    pressure=load_csv(pressure_url)
    temp_url="https://drive.google.com/file/d/1-2CRHi_OnqQwxEIrH06giexBEwkFKHjt/view?usp=sharing"
    temp=load_csv(temp_url)
    wind_direction_url="https://drive.google.com/file/d/1AeCMKxwX-gDnOQOyYJvBTreU0lFvf-yi/view?usp=sharing"
    wind_direction=load_csv(wind_direction_url)
    wind_speed_url="https://drive.google.com/file/d/1zYkIQtKO34UEILfNeIpPCnfIwCtZcmzD/view?usp=sharing"
    wind_speed=load_csv(wind_speed_url)
    
    city.columns="city"+city.columns
    weather_desc.columns="weather"+weather_desc.columns
    humidity.columns="humidity"+humidity.columns
    pressure.columns="pressure"+pressure.columns
    temp.columns="temp"+temp.columns
    wind_direction.columns="wind_direction"+wind_direction.columns
    wind_speed.columns="wind_speed"+wind_speed.columns
    data=pd.concat([city,weather_desc,humidity,pressure,temp,wind_direction,wind_speed],axis=1)
    montreal=data[data.columns[data.columns.str.contains("Montreal|citydate")]]
    return(city,weather_desc,humidity,pressure,temp,wind_direction,wind_speed,montreal)


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


##########NEW##########
#takes the montreal df as input and imputes the columns
def impute(df = montreal):
  df = df.drop(0) #dropping first row of nulls

  for col in list(df.drop(['citydatetime', 'weatherMontreal'], axis = 1).columns): #run iterative imputer on each column
    imp = IterativeImputer(random_state = 6)
    df[[col]] = imp.fit_transform(df[[col]])

  return df
