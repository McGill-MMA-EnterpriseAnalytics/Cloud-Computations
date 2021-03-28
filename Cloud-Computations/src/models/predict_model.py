
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


def predict_model(model_name, X_test):
    """
    """
    logger = logging.getLogger(__name__)
    logger.info('predicting')
    import pickle
    model = pickle.load(open("../../models/"+model_name+".pkl", 'rb'))
    scaler = pickle.load(open("../../models/"+model_name+"transformer.pkl", 'rb'))

    X_test_scaled = scaler.transform(X_test)
    X_test = pd.DataFrame(X_test_scaled)
    pred = model.predict(X_test)
    return(pred)
