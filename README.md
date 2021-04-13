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
3. The best explanatory factor for temperature will simply be the most recent available past temperatures.


## Table of Contents: 

**Section 1: Data Preparation**
- Data extraction 
- Data cleansing & preprocessing

- EDA

Descriptive weather events versus temperature

![Screen Shot 2021-04-12 at 7 43 45 PM](https://user-images.githubusercontent.com/78383866/114478071-78115400-9bcb-11eb-9e16-57f9ea5149a6.png)

Feature histograms broken down by weather events 

![Screen Shot 2021-04-12 at 7 47 38 PM](https://user-images.githubusercontent.com/78383866/114478102-91b29b80-9bcb-11eb-8699-21a107edf0f2.png)

Hourly, monthly, weekly Trend analysis 

![Screen Shot 2021-04-12 at 7 47 15 PM](https://user-images.githubusercontent.com/78383866/114478276-e229f900-9bcb-11eb-8e56-16003af65798.png)

Daily Temperature plot brokwn down by actual, minimum and maximum

![Screen Shot 2021-04-12 at 7 49 54 PM](https://user-images.githubusercontent.com/78383866/114478213-c0307680-9bcb-11eb-8eeb-9991c4456188.png)

- Feature Engineering: 
    - time point extraction, 
    - lagged features, 
    - [max,min,average]X[daily,weekly,monthly]X[temp,humidity,wind direction/speed] from the previous time point
        - ie. max daily temp, min daily temp, average daily temp, max weekly temp, min weekly temp,...etc
    - rolling and expanding window

Rolling Window

![Rolling Window Animation](https://cdn.analyticsvidhya.com/wp-content/uploads/2019/11/3hotmk.gif)

Expanding Window

![Expanding Window Animation](https://cdn.analyticsvidhya.com/wp-content/uploads/2019/12/output_B4KHcT.gif)

- Feature Selection using RFE

Sample RFE output

![Screen Shot 2021-04-12 at 8 06 07 PM](https://user-images.githubusercontent.com/78383866/114477888-151fbd00-9bcb-11eb-899d-6ab89ec5ad98.png)



**Section 2: Parametric Models**
- Autoregressive Integrative Moving Average (ARIMA) 
- Generalized Additive Model 

<img width="969" alt="Screen Shot 2021-04-13 at 9 41 49 AM" src="https://user-images.githubusercontent.com/75393332/114562505-8cda0000-9c3c-11eb-9075-8b5f6b84ab5a.png">


**Section 3: Machine Learning Models**
- XGBoost
- Random Forest
- Other Machine Learning Models
    
**Section 4: Neural Network Models**

Results contained within the RNN Daily Aggregation notebook and the Anomaly Detection Daily Aggregate notebook. The LSTM and Transformer models are created and tested in RNN Daily Aggregation. Autoencoders and anomaly detection are contained within the Anomaly Detection Daily Aggregate notebook.
- LSTM
![LSTM model sample output](https://github.com/hoganj15/MMA_Assignment_Data/blob/main/INSY695/Screen%20Shot%202021-04-12%20at%205.54.44%20PM.png)
- Transformers 
![Transformer model sample output](https://github.com/hoganj15/MMA_Assignment_Data/blob/main/INSY695/Screen%20Shot%202021-04-12%20at%206.01.26%20PM.png)
- Anomaly detection using Autoencoders 
![Anomaly detection sample output](https://github.com/hoganj15/MMA_Assignment_Data/blob/main/INSY695/Screen%20Shot%202021-04-12%20at%206.03.30%20PM.png)
    
**Section 5: AutoML**
- AutoML using Ludwig
    
**Section 6: Causal Inference** 
- Causal Inference using DoWhy

## Conclusion and Next Steps 

In conclusion, we proved that the best explanatory variables were indeed past temperature. However, neural networks did not perform best with a large variety of predictors. We did find though, that adding features to the XGBoost model did improve performance a bit. Lastly, the ARIMA model did not outperform XGBoost as we have originally thought. To conclude, the major threats to our model formulation is applying it to different locations, as geographical region can have a large impact on variable interactions. In our next steps, we would like to test the models and explore causal inference for different cities and quantify to what degree having multiple models for different cities is indeed beneficial (relative to a single model applied to all). We would also like to explore multi step forecasting for long-range forecasting purposes. 
