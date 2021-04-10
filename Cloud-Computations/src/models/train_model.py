import pandas as pd
import numpy as np
import os
import platform as pf
pd.options.mode.chained_assignment = None  # default='warn'

#packages for time series
import warnings
import itertools    
import statsmodels.api as sm

#Richard was here
from datetime import timedelta
from dateutil.relativedelta import relativedelta
import matplotlib.pyplot as plt
import math
from scipy import stats
import click
import logging
from pathlib import Path
from dotenv import find_dotenv, load_dotenv
import mlflow
import mlflow.sklearn


cwd = os.getcwd()
os_type = pf.system()



def train_test_split(data, n_test):
    return data[:n_test], data[n_test:]

def get_data(filename):
    df = pd.read_csv('../../data/processed/'+filename)
    return(df)

@click.command()
# @click.argument('input_filepath', type=click.Path(exists=True))
@click.argument('file_name', type=click.STRING)
@click.argument('model_name', type=click.STRING)
def main(file_name, model_name):
    """ Runs data processing scripts to turn raw data from (../raw) into
        cleaned data ready to be analyzed (saved in ../processed).
    """
    logger = logging.getLogger(__name__)
    logger.info('training final data set from processed data')
    df = get_data(file_name)
    df['datetime'] = df['datetime'].astype('datetime64[ns]')
    weather_df = df[['datetime', 'Temperature']].set_index('datetime')
    ml_df = pd.DataFrame({'Temperature': weather_df['Temperature']}, index = weather_df.index)

    # CREATE LAGGED ATTRIBUTES

    ml_df['date'] = ml_df.index
    ml_df['month'] = ml_df['date'].dt.day
    ml_df['month'] = ml_df['date'].dt.month
    ml_df['year'] = ml_df['date'].dt.year

    ml_df['lag1'] = ml_df['Temperature'].shift(periods=1, fill_value=0)
    ml_df['lag2'] = ml_df['Temperature'].shift(periods=2, fill_value=0)
    ml_df['lag12'] = ml_df['Temperature'].shift(periods=12, fill_value=0)
    ml_df['lag24'] = ml_df['Temperature'].shift(periods=24, fill_value=0)

    ml_df['avg_returns'] = 0
    for i in range(1, len(ml_df)):
        ml_df['avg_returns'][i] = ml_df['lag1'][:i + 1].mean()

    ml_df.drop('date', axis=1, inplace=True)

    # we have to eliminate all those with 0s
    ml_df = ml_df[ml_df['lag24'] != 0]
    X = ml_df.iloc[:,1:]
    y = ml_df[['Temperature']]
    split_len = int(len(weather_df)*0.80)

    X_train, X_test = train_test_split(X, split_len)
    y_train, y_test = train_test_split(y, split_len)

    from sklearn.preprocessing import StandardScaler

    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_train = pd.DataFrame(X_train_scaled)

    X_test_scaled = scaler.transform(X_test)
    X_test = pd.DataFrame(X_test_scaled)
    # with mlflow.start_run():
    import xgboost as xgb

    xgb_model = xgb.XGBRegressor(n_estimators=1000)
    xgb_model.fit(X_train, y_train,
                  eval_set=[(X_train, y_train), (X_test, y_test)],
                  early_stopping_rounds=50,
                  verbose=False)
    pred = xgb_model.predict(X_test)
    ts_results = pd.DataFrame({'Predicted': pred, 'Observed': y_test['Temperature']})
    ts_results[ts_results['Predicted'] <= 0] = 0
    ts_results['RMSE'] = np.sqrt((ts_results['Predicted'] - ts_results['Observed']) ** 2)
    ts_results['RMSE'].mean()

    logger.info('RMSE:' + str(ts_results['RMSE'].mean()))

    import pickle
    print("DONE")
    pickle.dump(xgb_model, open("../../models/"+model_name+".pkl", 'wb'))
    pickle.dump(scaler, open("../../models/"+model_name+"transformer.pkl", 'wb'))
    pickle.dump(xgb_model, open(model_name+".pkl", 'wb'))
    pickle.dump(scaler, open(model_name+"transformer.pkl", 'wb'))

if __name__ == '__main__':
    log_fmt = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    logging.basicConfig(level=logging.INFO, format=log_fmt)

    # not used in this stub but often useful for finding various files
    project_dir = Path(__file__).resolve().parents[2]

    # find .env automagically by walking up directories until it's found, then
    # load up the .env entries as environment variables
    load_dotenv(find_dotenv())

    main()





