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
ssl._create_default_https_context = ssl._create_unverified_context
def load_csv(url):
    orig_url=url
    file_id = 'https://drive.google.com/uc?export=download&id='+orig_url.split('/')[-2]
    dfs = pd.read_csv(file_id,error_bad_lines=False)
    return(dfs)

def load_data(df):
    if(df=='city'):
        city_url="https://drive.google.com/file/d/1zYkIQtKO34UEILfNeIpPCnfIwCtZcmzD/view?usp=sharing"
        city=load_csv(city_url)
        return(city)
    elif(df=='weather'):
        
        weather_desc_url="https://drive.google.com/file/d/1-9uMFJnLZSJLdyZeST6G2AArtR--yMJa/view?usp=sharing"
        weather_desc=load_csv(weather_desc_url)
        return(weather_desc)
    elif(df=='humidity'):
        
        humidity_url="https://drive.google.com/file/d/1-38LryQSt16wh4JXteC049sHWYqoyc3d/view?usp=sharing"
        humidity=load_csv(humidity_url)
        return(humidity)
    elif(df=="pressure"):
        
        pressure_url="https://drive.google.com/file/d/1-1ZCUKvf6LE7BBQnchnBk4U5Q0qO58IY/view?usp=sharing"
        pressure=load_csv(pressure_url)
        return(pressure)
    elif(df=="temp"):
        
        temp_url="https://drive.google.com/file/d/1-2CRHi_OnqQwxEIrH06giexBEwkFKHjt/view?usp=sharing"
        temp=load_csv(temp_url)
        return(temp)
    elif(df=="wind_direction"): 
        
        wind_direction_url="https://drive.google.com/file/d/1AeCMKxwX-gDnOQOyYJvBTreU0lFvf-yi/view?usp=sharing"
        wind_direction=load_csv(wind_direction_url)
        return(wind_direction)
    elif(df=="wind_speed"):
       
        wind_speed_url="https://drive.google.com/file/d/1zYkIQtKO34UEILfNeIpPCnfIwCtZcmzD/view?usp=sharing"
        wind_speed=load_csv(wind_speed_url)
        return(wind_speed)
    else:
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
        return(montreal)


def api(city):
    API_KEY=os.getenv('WEATHER_API')
    r = requests.get('http://api.openweathermap.org/data/2.5/weather?q='+city+'&APPID=484925ef3995e2026aa4d24818ac18b1')
    from pandas import json_normalize 

    response=json.loads(r.text)
    response_cols=response.keys()
    data=json_normalize(json.loads(r.text))
    weather=json_normalize(json.loads(r.text),record_path=['weather'])
    weather.columns='weather.'+weather.columns
    final_data=pd.concat([data[data.columns[1:len(data.columns)]],weather],axis=1)
    return(final_data)


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
def load_data_all(df):
    data=load_data(df)
    return(data)



select=st.selectbox("What Data",["All",'city','weather','humidity','pressure','temp','wind_direction','wind_speed'])

    

data=load_data_all(select)
feature_x = st.selectbox("X Axis",data.columns)
feature_y = st.selectbox("Y Axis",data.columns)
hover_data=st.selectbox("Hover Data",data.columns)
size=st.selectbox("Size",data.columns)
color=st.selectbox("Color",data.columns)

st.write(data)
fig = px.scatter(data.loc[0:50000], x=feature_x, y=feature_y)# size=size, hover_data=[hover_data],color=color)
st.write(fig)
    
api_city=st.text_input("API City Current Weather","Montreal")
api_df=api(api_city)
st.write(api_df)


# HtmlFile = open("../"+str(select)+".html", 'r', encoding='utf-8')
# source_code = HtmlFile.read() 
# components.html(source_code)
    
    