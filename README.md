# INSY 695 - Enterprise Data Science 
## Team: Cloud Computations
## Topic: Weather Prediction: A Case Study on Montreal, Quebec

### Team Members:
- Richard Gao -- 260729805
- Jake Hogan -- 260731171
- Steven Liang -- 
- Hanna Swail -- 260746086
- Duncan Wang -- 260710229


## Introduction 


The ability to produce accurate weather forecasts remains a crucial social and economic priority, with benefits cascading across sectors including transportation, tourism, and agriculture. The US Weather Service estimates that investment in public weather forecasts has an annualized benefit of over $31 billion (Lazo et al. 2009).

Classical approaches to weather forecasting by meteorologists use complex climatological models constructed from data collected from a large range of sources, from weather stations, to balloons, to radar and satellites. Because of this, access to good forecasts can be geographically constrained. While these models have been successful, there is still a significant opportunity for machine and deep learning models to improve the accuracy and geographic availability of traditional weather forecasting. 

## Objective 

The objective of this project is to use historical time-series data to predict future average hourly and daily temperatures (in Celcius) in Montreal, explain what factors are driving local weather patterns, and see how our forecasts compare to the accuracy of current forecasts. We will be exploring several parametric, machine learning, and deep learning models, and comparing their relative performances. We will also use causal inference methods to examine driving factors, and utilize exogenous data streams and anomaly detection methods to improve prediction accuracy. 

## Hypotheses

We form the following 3 hypotheses:
1. Simple parametric models such as ARIMA will have a lower prediction error than more complicated machine learning or neural network models when given just past temperature patterns as a predictor to forecast future temperatures with (with no exogenous variables) 
2. Neural Network models will perform best when a large variety of predictors are available, since they are generally more capable of identifying and capturing any hidden variable relationships, when present, that might not be visible to the human eye.
2. The best explanatory factor for temperature will simply be the most recent available past temperatures.


## Table of Contents: 

**Section 1: Data Preparation**
- Data extraction 
- Data cleansing & preprocessing
- EDA
- Feature Engineering

**Section 2: Parametric Models**
- Autoregressive Integrative Moving Average (ARIMA) 
- Generalized Additive Model 

**Section 3: Machine Learning Models**
- XGBoost
- Random Forest
- Other Machine Learning Models
    
**Section 4: Neural Network Models**
- LSTM
- Transformers 
- Anomaly detection using Autoencoders 
    
**Section 5: AutoML**
- AutoML using Ludwig
    
**Section 6: Causal Inference** 
- Causal Inference using DoWhy
