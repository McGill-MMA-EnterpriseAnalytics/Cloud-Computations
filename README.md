
# INSY 695 - Enterprise Data Science 
## Team: Cloud Computations
## Topic: Weather Prediction: A Case Study on Montreal, Quebec

### Team Members:
- Richard Gao -- 260729805
- Jake Hogan -- 260731171
- Steven Liang -- 260415672
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

**Section 2: Parametric Models**

**Section 3: Machine Learning Models**

**Section 4: Neural Network Models**

**Section 5: AutoML**

**Section 6: Causal Inference** 

## Important Notebooks: 
- [Parametric Models](https://github.com/McGill-MMA-EnterpriseAnalytics/Cloud-Computations/blob/Features/INSY695_ParametricModels.ipynb) 
- [Machine Learning Models](https://github.com/McGill-MMA-EnterpriseAnalytics/Cloud-Computations/blob/Features/INSY695_MLModels.ipynb) 
- [AutoML Models](https://github.com/McGill-MMA-EnterpriseAnalytics/Cloud-Computations/blob/Features/INSY695_AutoMLModels.ipynb)
- [Causal Inference](https://github.com/McGill-MMA-EnterpriseAnalytics/Cloud-Computations/blob/Features/Causal%20Inference.ipynb)
- [Presentation Deck](https://github.com/McGill-MMA-EnterpriseAnalytics/Cloud-Computations/tree/main/Powerpoints)
- [RNN Daily Aggregation](https://github.com/McGill-MMA-EnterpriseAnalytics/Cloud-Computations/blob/Features/RNN%20Daily%20Aggregation.ipynb)
- [Anomaly Detection Daily Aggregate](https://github.com/McGill-MMA-EnterpriseAnalytics/Cloud-Computations/blob/Features/Anomaly%20Detection%20Daily%20Aggregate.ipynb)



## Data Source

[Access the data here](https://www.kaggle.com/selfishgene/historical-hourly-weather-data) 

## Methods 

### Section 1: Data Preparation
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



### Section 2: Parametric Models
- Autoregressive Integrative Moving Average (ARIMA) 
- Generalized Additive Model 

**Seasonal ARIMA**

A seasonal ARIMA model was built using a process of gridsearch to determine the optimal seasonal and non-seasonal ARIMA Autoregression (A), Integration (I), and Moving Average (MA) parameters required. The simple ARIMA achieved a MAE of 2.57. 
<img width="969" alt="Screen Shot 2021-04-13 at 9 41 49 AM" src="https://user-images.githubusercontent.com/75393332/114562505-8cda0000-9c3c-11eb-9075-8b5f6b84ab5a.png">

**Generalized Additive Model**
The Generalized Additive Model was built using Facebook's forecasting tool, Prophet, which achieved an MAE of 3.75. We see this case that ARIMA performs better, as it appears to fit the daily fluctuations better than the GAM model, which generalizes the pattern but misses the ups and downs. We propose this could because GAM uses a sum of smooth functions & a process of backfitting to fit a trend line. 

<img width="959" alt="Screen Shot 2021-04-13 at 9 42 01 AM" src="https://user-images.githubusercontent.com/75393332/114562687-b7c45400-9c3c-11eb-822a-e623adbf8823.png">


### Section 3: Machine Learning Models

A variety of Machine Learning models were fit, using both a simple set of features consisting of different combinations of the lagged past values of temperature and time components, as well as a more complex set of features including humidity, windspeed, and wind direction. We also performed Bayesian hyperparameter optimization using Hyperopt to further tune the models. Overall, XGBoost was best at identifying important predictors and benefited from the information given by a more comprehensive feature set, but hyperparameter tuning had little to no effect on the model. The best XGBoost model with an increased feature set obtained an MAE of 2.42, but the simple XGBoost model performed worse, with an MAE of 2.77. 


![Screen Shot 2021-04-13 at 10 13 56 AM](https://user-images.githubusercontent.com/75393332/114567187-fa882b00-9c40-11eb-8437-6b3780c948bb.png)


![Screen Shot 2021-04-13 at 10 14 36 AM](https://user-images.githubusercontent.com/75393332/114567339-24d9e880-9c41-11eb-8500-16fed0d120e0.png)

**SHAP Analysis**: 
We also used SHAP for feature importance interpretation:

Initial Summary: Lag1 is are most important predictor (consistent with regular feature importance)

![Initial Summary](https://github.com/StevenYML/EnterpriseII/blob/main/SHAP%20Summary%201%20Screenshot%202021-04-13%20143014.png)

Depedence Plots:
* We see the strong direct linear proportional relationship lag1 and predictions

![dep deplot 1](https://github.com/StevenYML/EnterpriseII/blob/main/SHAP%20Dep%20Plot%201%20Screenshot%202021-04-13%20143014.png)

We can also see where it start to diverge, if we looked at lag12 for instance
* The relationship is similar but is not as strong
* There are a lot more outliers
* Especially with low lag12 temperatures can be associated with a big range of low to high temperature predictions

![dep plot 2](https://github.com/StevenYML/EnterpriseII/blob/main/SHAP%20Dep%20Plot%202%202021-04-13%20143105.png)

Whether we added more or less features, lag1 stayed the #1 predictor.

![SHAP Summary 2](https://github.com/StevenYML/EnterpriseII/blob/main/SHAP%20Summary%202%20Screenshot%202021-04-13%20143014.png)
![SHAP Summary 3](https://github.com/StevenYML/EnterpriseII/blob/main/SHAP%20Summary%203%20Screenshot%202021-04-13%20143014.png)







    
### Section 4: Neural Network Models

Results contained within the [RNN Daily Aggregation notebook](https://github.com/McGill-MMA-EnterpriseAnalytics/Cloud-Computations/blob/Features/RNN%20Daily%20Aggregation.ipynb) and the [Anomaly Detection Daily Aggregate notebook](https://github.com/McGill-MMA-EnterpriseAnalytics/Cloud-Computations/blob/Features/Anomaly%20Detection%20Daily%20Aggregate.ipynb). The LSTM and Transformer models are created and tested in RNN Daily Aggregation. Autoencoders and anomaly detection are contained within the Anomaly Detection Daily Aggregate notebook.
- LSTM
![LSTM model sample output](https://github.com/hoganj15/MMA_Assignment_Data/blob/main/INSY695/Screen%20Shot%202021-04-12%20at%205.54.44%20PM.png)
- Transformers 
![Transformer model sample output](https://github.com/hoganj15/MMA_Assignment_Data/blob/main/INSY695/Screen%20Shot%202021-04-12%20at%206.01.26%20PM.png)
- Anomaly detection using Autoencoders 
![Anomaly detection sample output](https://github.com/hoganj15/MMA_Assignment_Data/blob/main/INSY695/Screen%20Shot%202021-04-12%20at%206.03.30%20PM.png)
    
### Section 5: AutoML

We also compared our RNN results with an RNN AutoML model built using Ludwig, which obtained a MAE of 2.85. 

![Screen Shot 2021-04-13 at 10 16 18 AM](https://user-images.githubusercontent.com/75393332/114567503-4dfa7900-9c41-11eb-943a-f4700a5ee707.png)

![Screen Shot 2021-04-13 at 10 15 56 AM](https://user-images.githubusercontent.com/75393332/114567519-50f56980-9c41-11eb-9d54-16d83d553a88.png)


    
### Section 6: Causal Inference (DoWhy)
There was a lot of experiemntation with this section as our initial results were pretty strange looking and distorted. We see that overall, there's not that much of an impact at all from our regular features we fed into the ML models. We believe that there are a few issues that are causing this:

* Due to the nature of our project, the data we are working with comes with specific data profiles such as temperature being cyclical and also features such as humidity, windspeed/direction, pressure exist in all types of temperature ranges...leading to a causal result that's near zero.

* We have many feature that are engineered. Here we are using what we fed into some of our initial model trial runs, and we see that with causal inference, it's not easy to interpret. While this is the initial test, subsequent test will have to be more narrow in terms of what we want to see and push into DoWhy. We will be choosing our features more carefully and also be more mindful of feature engineering for specific features.

Inital Results :
![Initial Causal Inference Output - Filtered for Significant Features](https://github.com/StevenYML/EnterpriseII/blob/main/Screenshot%202021-04-13%20141922.png)

Final Results - Through careful feature selection and engineering
* Creation of seasons variables for intperpreability
* Changing continous variables like pressure, wind speed and humidity into categorical low, medium and high categories through quanitiles.
* Dropping the medium category to keep the data with the highest variance.

![Final Causal Inference Output](https://github.com/StevenYML/EnterpriseII/blob/main/Screenshot%202021-04-13%20141402.png)

These results above look much better in terms of treatment effects on temperature.

* High Pressure = cold vs Low Pressure
* High Humidity = warmer vs low humidity
* Wind Speed = no difference high vs low

Other Insights:

* Autume is warmer than spring
* Winter = cold, Summer = hot
> * While "Winter = cold, Summer = hot" might seem like a no brainer to us, keep in mind that keep in mind that a computer doesn't know what the concept summer and winter is, and that seeing results that we know are good is not something we should take for granted. If anything it goes back to the trust and transparency topic we covered a while back - seeing obvious results give confidence for other insight the model provides which are good.

Weather Patterns on Temperature:

* Snow is causes with cooler temperatures
* Thunderstorms cause warmer temperatures
* Most other weather patterns are on the warm side too.

Which makes sense for precipitation.

## Conclusion and Next Steps 

In conclusion, we proved that the best explanatory variables were indeed past temperature. However, neural networks did not perform best with a large variety of predictors. We did find though, that adding features to the XGBoost model did improve performance a bit. Lastly, the ARIMA model outperform XGBoost as we had originally thought, with a simple set of features, but XGBoost performed the best overall since it was more easily able to take advantage of a larger set of features. To conclude, the major threats to our model formulation is applying it to different locations, as geographical region can have a large impact on variable interactions. In our next steps, we would like to test the models and explore causal inference for different cities and quantify to what degree having multiple models for different cities is indeed beneficial (relative to a single model applied to all). We would also like to explore multi step forecasting for long-range forecasting purposes. 
