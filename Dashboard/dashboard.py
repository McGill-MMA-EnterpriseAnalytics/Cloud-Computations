import numpy as np
import pandas as pd
import streamlit as st
import streamlit.components.v1 as components
import matplotlib.pyplot as plt
import pickle
from pandas_profiling import ProfileReport
import seaborn as sns
import plotly.express as px
import plotly.figure_factory as ff
from pprint import pprint
import requests
import os
import requests
from io import StringIO
import ssl
import json
from pandas_profiling import ProfileReport

import sys
# sys.path.append("../")
# import helper
ssl._create_default_https_context = ssl._create_unverified_context
# def load_csv(url):
#     orig_url=url
#     file_id = 'https://drive.google.com/uc?export=download&id='+orig_url.split('/')[-2]
#     dfs = pd.read_csv(file_id,error_bad_lines=False)
#     return(dfs)

# def load_data(df):
#     if(df=='city'):
#         city_url="https://drive.google.com/file/d/1zYkIQtKO34UEILfNeIpPCnfIwCtZcmzD/view?usp=sharing"
#         city=load_csv(city_url)
#         return(city)
#     elif(df=='weather'):
#
#         weather_desc_url="https://drive.google.com/file/d/1-9uMFJnLZSJLdyZeST6G2AArtR--yMJa/view?usp=sharing"
#         weather_desc=load_csv(weather_desc_url)
#         return(weather_desc)
#
#     elif(df=='humidity'):
#
#         humidity_url="https://drive.google.com/file/d/1-38LryQSt16wh4JXteC049sHWYqoyc3d/view?usp=sharing"
#         humidity=load_csv(humidity_url)
#         return(humidity)
#     elif(df=="pressure"):
#
#         pressure_url="https://drive.google.com/file/d/1-1ZCUKvf6LE7BBQnchnBk4U5Q0qO58IY/view?usp=sharing"
#         pressure=load_csv(pressure_url)
#         return(pressure)
#     elif(df=="temp"):
#
#         temp_url="https://drive.google.com/file/d/1-2CRHi_OnqQwxEIrH06giexBEwkFKHjt/view?usp=sharing"
#         temp=load_csv(temp_url)
#         return(temp)
#     elif(df=="wind_direction"):
#
#         wind_direction_url="https://drive.google.com/file/d/1AeCMKxwX-gDnOQOyYJvBTreU0lFvf-yi/view?usp=sharing"
#         wind_direction=load_csv(wind_direction_url)
#         return(wind_direction)
#     elif(df=="wind_speed"):
#
#         wind_speed_url="https://drive.google.com/file/d/1zYkIQtKO34UEILfNeIpPCnfIwCtZcmzD/view?usp=sharing"
#         wind_speed=load_csv(wind_speed_url)
#         return(wind_speed)
#     else:
#         city_url="https://drive.google.com/file/d/1zYkIQtKO34UEILfNeIpPCnfIwCtZcmzD/view?usp=sharing"
#         city=load_csv(city_url)
#         weather_desc_url="https://drive.google.com/file/d/1-9uMFJnLZSJLdyZeST6G2AArtR--yMJa/view?usp=sharing"
#         weather_desc=load_csv(weather_desc_url)
#         humidity_url="https://drive.google.com/file/d/1-38LryQSt16wh4JXteC049sHWYqoyc3d/view?usp=sharing"
#         humidity=load_csv(humidity_url)
#         pressure_url="https://drive.google.com/file/d/1-1ZCUKvf6LE7BBQnchnBk4U5Q0qO58IY/view?usp=sharing"
#         pressure=load_csv(pressure_url)
#         temp_url="https://drive.google.com/file/d/1-2CRHi_OnqQwxEIrH06giexBEwkFKHjt/view?usp=sharing"
#         temp=load_csv(temp_url)
#         wind_direction_url="https://drive.google.com/file/d/1AeCMKxwX-gDnOQOyYJvBTreU0lFvf-yi/view?usp=sharing"
#         wind_direction=load_csv(wind_direction_url)
#         wind_speed_url="https://drive.google.com/file/d/1zYkIQtKO34UEILfNeIpPCnfIwCtZcmzD/view?usp=sharing"
#         wind_speed=load_csv(wind_speed_url)
#         city.columns="city"+city.columns
#         weather_desc.columns="weather"+weather_desc.columns
#         humidity.columns="humidity"+humidity.columns
#         pressure.columns="pressure"+pressure.columns
#         temp.columns="temp"+temp.columns
#         wind_direction.columns="wind_direction"+wind_direction.columns
#         wind_speed.columns="wind_speed"+wind_speed.columns
#         data=pd.concat([city,weather_desc,humidity,pressure,temp,wind_direction,wind_speed],axis=1)
#         montreal=data[data.columns[data.columns.str.contains("Montreal|citydate")]]
#         return(montreal)
def load_data(city):
    data=pd.read_csv("../Cloud-Computations/src/data/processed/"+city+".csv")
    return(data)

def api(city):
    API_KEY=os.getenv('WEATHER_API')
    r = requests.get('http://api.openweathermap.org/data/2.5/weather?q='+city+'&APPID=484925ef3995e2026aa4d24818ac18b1')
    from pandas import json_normalize 

    response=json.loads(r.text)
    response_cols=response.keys()
    print(response)
    data=json_normalize(json.loads(r.text))
    weather=json_normalize(json.loads(r.text),record_path=['weather'])
    weather.columns='weather.'+weather.columns
    final_data=pd.concat([data[data.columns[1:len(data.columns)]],weather],axis=1)
    return(final_data)

def api2(city):
    lat = '45.5088'
    lon = '-73.5878'
    city = "Montreal"
    API_KEY = os.getenv('WEATHER_API')
    r = requests.get(
        'http://api.openweathermap.org/data/2.5/onecall?lat=' + lat + '&lon=' + lon + '&APPID=484925ef3995e2026aa4d24818ac18b1')
    from pandas import json_normalize

    response = json.loads(r.text)
    response_cols = response.keys()
    data = json_normalize(json.loads(r.text))

    # weather=json_normalize(json.loads(r.text),record_path=['weather'])
    # weather.columns='weather.'+weather.columns
    # final_data=pd.concat([data[data.columns[1:len(data.columns)]],weather],axis=1)
    return(pd.DataFrame(data['hourly'][0]))


admin = False
c1 = st.sidebar.checkbox('Admin Mode', False)

st.title('Weather Data')

if c1:
    admin = True
      # st.sidebar.text(admin)
else:
    admin = False
    # st.sidebar.text(admin)
    
@st.cache(persist=True, allow_output_mutation=True)
def load_data_all(city):
    data=load_data(city)
    data['datetime']= pd.to_datetime(data['datetime'])
    return(data)


from datetime import datetime

select=st.selectbox("What Data",["Montreal"])
data=load_data_all(select)
# year = st.slider("Year", min(data['year']), max(data['year']), (min(data['year']), min(data['year']+1)), 1)
date1 = st.sidebar.date_input('start date', data['datetime'][0])
date2 = st.sidebar.date_input('start date', data['datetime'][1000])
year1 = date1.year
year2 = date2.year
month1 = date1.month
month2 = date2.month
day1 = date1.day
day2 = date2.day

date1 = pd.Timestamp(str(year1) + "-"+str(month1) +"-"+str(day1)+' 00:00:00')
date2 = pd.Timestamp(str(year2) + "-"+str(month2) +"-"+str(day2)+' 00:00:00')

data = data[(data['datetime'] >= date1) & (data['datetime'] <= date2)]
print(data.columns)
x_cols = ['datetime', 'Description', 'Humidity', 'Wind Direction', 'Temperature',
       'Pressure', 'Wind Speed', 'clouds', 'rain', 'mist', 'snow', 'shower',
       'thunderstorm', 'fog', 'other', 'Intensity', 'year', 'month', 'day',
       'hour', 'minute', 'weekday', 'week', 'quarter', 'month start',
       'month end', 'quarter start', 'quarter end', 'lag1', 'lag2', 'lag12',
       'lag30', 'max daily temp', 'max daily hum', 'max daily wind speed',
       'max daily wind direction', 'max daily pressure', 'max weekly temp',
       'max weekly hum', 'max weekly wind speed', 'max weekly wind direction',
       'max weekly pressure', 'min daily temp', 'min daily hum',
       'min daily wind speed', 'min daily wind direction',
       'min daily pressure', 'min weekly temp', 'min weekly hum',
       'min weekly wind speed', 'min weekly wind direction',
       'min weekly pressure', 'mean daily temp', 'mean daily hum',
       'mean daily wind speed', 'mean daily wind direction',
       'mean daily pressure', 'mean weekly temp', 'mean weekly hum',
       'mean weekly wind speed', 'mean weekly wind direction',
       'mean weekly pressure', 'rolling_mean_temp', 'rolling_mean_pressure',
       'rolling_mean_wind_dir', 'rolling_mean_wind_speed',
       'rolling_mean_humidity', 'rolling_min_temp', 'rolling_min_pressure',
       'rolling_min_wind_dir', 'rolling_min_wind_speed',
       'rolling_min_humidity', 'rolling_max_temp', 'rolling_max_pressure',
       'rolling_max_wind_dir', 'rolling_max_wind_speed',
       'rolling_max_humidity']
y_cols = ['Temperature', 'datetime', 'Description', 'Humidity', 'Wind Direction',
       'Pressure', 'Wind Speed', 'clouds', 'rain', 'mist', 'snow', 'shower',
       'thunderstorm', 'fog', 'other', 'Intensity', 'year', 'month', 'day',
       'hour', 'minute', 'weekday', 'week', 'quarter', 'month start',
       'month end', 'quarter start', 'quarter end', 'lag1', 'lag2', 'lag12',
       'lag30', 'max daily temp', 'max daily hum', 'max daily wind speed',
       'max daily wind direction', 'max daily pressure', 'max weekly temp',
       'max weekly hum', 'max weekly wind speed', 'max weekly wind direction',
       'max weekly pressure', 'min daily temp', 'min daily hum',
       'min daily wind speed', 'min daily wind direction',
       'min daily pressure', 'min weekly temp', 'min weekly hum',
       'min weekly wind speed', 'min weekly wind direction',
       'min weekly pressure', 'mean daily temp', 'mean daily hum',
       'mean daily wind speed', 'mean daily wind direction',
       'mean daily pressure', 'mean weekly temp', 'mean weekly hum',
       'mean weekly wind speed', 'mean weekly wind direction',
       'mean weekly pressure', 'rolling_mean_temp', 'rolling_mean_pressure',
       'rolling_mean_wind_dir', 'rolling_mean_wind_speed',
       'rolling_mean_humidity', 'rolling_min_temp', 'rolling_min_pressure',
       'rolling_min_wind_dir', 'rolling_min_wind_speed',
       'rolling_min_humidity', 'rolling_max_temp', 'rolling_max_pressure',
       'rolling_max_wind_dir', 'rolling_max_wind_speed',
       'rolling_max_humidity']
size_cols = ['Humidity', 'Temperature', 'datetime', 'Description', 'Wind Direction',
       'Pressure', 'Wind Speed', 'clouds', 'rain', 'mist', 'snow', 'shower',
       'thunderstorm', 'fog', 'other', 'Intensity', 'year', 'month', 'day',
       'hour', 'minute', 'weekday', 'week', 'quarter', 'month start',
       'month end', 'quarter start', 'quarter end', 'lag1', 'lag2', 'lag12',
       'lag30', 'max daily temp', 'max daily hum', 'max daily wind speed',
       'max daily wind direction', 'max daily pressure', 'max weekly temp',
       'max weekly hum', 'max weekly wind speed', 'max weekly wind direction',
       'max weekly pressure', 'min daily temp', 'min daily hum',
       'min daily wind speed', 'min daily wind direction',
       'min daily pressure', 'min weekly temp', 'min weekly hum',
       'min weekly wind speed', 'min weekly wind direction',
       'min weekly pressure', 'mean daily temp', 'mean daily hum',
       'mean daily wind speed', 'mean daily wind direction',
       'mean daily pressure', 'mean weekly temp', 'mean weekly hum',
       'mean weekly wind speed', 'mean weekly wind direction',
       'mean weekly pressure', 'rolling_mean_temp', 'rolling_mean_pressure',
       'rolling_mean_wind_dir', 'rolling_mean_wind_speed',
       'rolling_mean_humidity', 'rolling_min_temp', 'rolling_min_pressure',
       'rolling_min_wind_dir', 'rolling_min_wind_speed',
       'rolling_min_humidity', 'rolling_max_temp', 'rolling_max_pressure',
       'rolling_max_wind_dir', 'rolling_max_wind_speed',
       'rolling_max_humidity']
color_cols = ['clouds', 'rain', 'mist', 'snow', 'shower',
       'thunderstorm', 'fog', 'other', 'Intensity', 'year', 'month', 'day',
       'hour', 'minute', 'weekday', 'week', 'quarter', 'month start',
       'month end', 'quarter start', 'quarter end', 'lag1', 'lag2', 'lag12',
       'lag30', 'max daily temp', 'max daily hum', 'max daily wind speed',
       'max daily wind direction', 'max daily pressure', 'max weekly temp',
       'max weekly hum', 'max weekly wind speed', 'max weekly wind direction',
       'max weekly pressure', 'min daily temp', 'min daily hum',
       'min daily wind speed', 'min daily wind direction',
       'min daily pressure', 'min weekly temp', 'min weekly hum',
       'min weekly wind speed', 'min weekly wind direction',
       'min weekly pressure', 'mean daily temp', 'mean daily hum',
       'mean daily wind speed', 'mean daily wind direction',
       'mean daily pressure', 'mean weekly temp', 'mean weekly hum',
       'mean weekly wind speed', 'mean weekly wind direction',
       'mean weekly pressure', 'rolling_mean_temp', 'rolling_mean_pressure',
       'rolling_mean_wind_dir', 'rolling_mean_wind_speed',
       'rolling_mean_humidity', 'rolling_min_temp', 'rolling_min_pressure',
       'rolling_min_wind_dir', 'rolling_min_wind_speed',
       'rolling_min_humidity', 'rolling_max_temp', 'rolling_max_pressure',
       'rolling_max_wind_dir', 'rolling_max_wind_speed',
       'rolling_max_humidity','Humidity', 'Temperature', 'datetime', 'Description', 'Wind Direction',
       'Pressure', 'Wind Speed']

def query_model(model,month,year,lag1,lag2,lag12,lag24,avg_returns):
    import requests

    headers = {
        'accept': 'application/json',
        'Content-Type': 'application/json',
    }

    data = '{ "model": "Montreal", "month": '+str(month)+', "year": '+str(year)+', "lag1": '+str(lag1)+', "lag2": '+str(lag2)+\
           ', "lag12": '+str(lag12)+', "lag24": '+str(lag24)+', "avg_returns": '+str(avg_returns)+' }'

    response = requests.post('http://localhost:8000/predict', headers=headers, data=data)
    return(response)

feature_x = st.selectbox("X Axis", x_cols)
feature_y = st.selectbox("Y Axis", y_cols)
hover_data=st.selectbox("Hover Data", data.columns)
# size=st.selectbox("Size",size_cols)
color=st.selectbox("Color",color_cols)

# st.write(data)
fig = px.scatter(data.loc[0:50000], x=feature_x, y=feature_y, hover_data=[hover_data],color=color)
st.write(fig)
st.header('** Temperature last 48 hours **')

# api_city=st.text_input("API City Current Weather","Montreal")
api_df=api2(select)
st.write(api_df)
month=datetime.now().month
year=datetime.now().year
lag1=api_df['temp'][api_df.index[len(api_df)-1]]
lag2=api_df['temp'][api_df.index[len(api_df)-2]]
lag12=api_df['temp'][api_df.index[len(api_df)-13]]
lag24=api_df['temp'][api_df.index[len(api_df)-25]]
avg_returns= sum(api_df['temp'])/len(api_df)
st.header('** Forecast for the next hour **')
forecast=json.loads(query_model(select,month,year,lag1,lag2,lag12,lag24,avg_returns).text)['forecast'].replace("[","").replace("]","")

st.write(forecast)


# HtmlFile = open("../"+str(select)+".html", 'r', encoding='utf-8')
# source_code = HtmlFile.read() 
# components.html(source_code)
    
    