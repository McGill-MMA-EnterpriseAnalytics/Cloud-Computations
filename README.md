## Weather Prediction

**Richard Gao, Jake Hogan, Steven Liang, Hanna Swail, & Duncan Wang**

The ability to produce accurate weather forecasts remains a crucial social and economic priority, with benefits cascading across sectors including transportation, tourism, and agriculture. The US Weather Service estimates that investment in public weather forecasts has an annualized benefit of over $31 billion (Lazo et al. 2009).

Classical approaches to weather forecasting by meteorologists use complex climatological models constructed from data collected from a large range of sources, from weather stations, to balloons, to radar and satellites. Because of this, access to good forecasts can be geographically constrained. While these models have been successful, there is still a significant opportunity for machine and deep learning models to improve the accuracy and geographic availability of traditional weather forecasting. 

The objective of this project is to use historical time-series data to predict average daily temperatures for the next week, and explain what factors are driving local weather patterns. We will be exploring several parametric (ARIMA), machine learning (XGBoost, Random Forest), and deep learning methods (RNN, LSTM), and comparing their relative performances. We will also use causal inference methods to examine driving factors, and utilize exogenous data streams and anomaly detection methods to improve prediction accuracy. 


MLFLOW:

mlflow server \
    --backend-store-uri sqlite:///mlflow.db \
    --default-artifact-root ./artifacts \
    --host 0.0.0.0
