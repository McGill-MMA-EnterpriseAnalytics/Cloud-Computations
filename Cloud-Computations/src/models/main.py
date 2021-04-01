from fastapi import FastAPI
import uvicorn
from sklearn.datasets import load_iris
from sklearn.naive_bayes import GaussianNB
from pydantic import BaseModel
# from predict_model import *
# Creating FastAPI instance

import pandas as pd
pd.options.mode.chained_assignment = None  # default='warn'
import logging

def predict_model(model_name, X_test):
    """
    """
    logger = logging.getLogger(__name__)
    logger.info('predicting')
    import pickle
    try:
        model = pickle.load(open("../../models/"+model_name+".pkl", 'rb'))
        scaler = pickle.load(open("../../models/"+model_name+"transformer.pkl", 'rb'))
    except:
        model = pickle.load(open(model_name + ".pkl", 'rb'))
        scaler = pickle.load(open(model_name + "transformer.pkl", 'rb'))

    print(type(scaler))
    X_test_scaled = scaler.transform(X_test)
    X_test = pd.DataFrame(X_test_scaled)
    pred = model.predict(X_test)
    return(pred)


app = FastAPI()


# Creating class to define the request body
# and the type hints of each attribute
class request_body(BaseModel):
    model: str
    month: float
    year: int
    lag1: float
    lag2: float
    lag12: float
    lag24: float
    avg_returns: float

# Loading Iris Dataset


# Creating and Fitting our Model


# Creating an Endpoint to recieve the data
# to make prediction on.
@app.post('/predict')
def predict(data: request_body):
    # Making the data in a form suitable for prediction
    import pickle

    test_data = [[
        data.month,
        data.year,
        data.lag1,
        data.lag2,
        data.lag12,
        data.lag24,
        data.avg_returns,
    ]]
    # import pandas as pd
    # # Predicting
    # if data.model == 'Montreal':
    #     clf = pickle.load(open('../../models/Montreal.pkl', 'rb'))
    # else:
    #     clf = pickle.load(open('../../models/Montreal.pkl', 'rb'))

    test_data = pd.DataFrame(test_data)
    forecast = predict_model(data.model, test_data) #clf.predict(pd.DataFrame(test_data))

    # Return the Result
    return {'forecast': str(forecast)}

if __name__ == '__main__':
    uvicorn.run(app, host='127.0.0.1', port=8000)