
import pandas as pd
pd.options.mode.chained_assignment = None  # default='warn'

import logging


def predict_model(model_name, X_test):
    """
    """
    logger = logging.getLogger(__name__)
    logger.info('predicting')
    import pickle
    model = pickle.load(open("../../models/"+model_name+".pkl", 'rb'))
    scaler = pickle.load(open("../../models/"+model_name+"transformer.pkl", 'rb'))
    print(type(scaler))
    X_test_scaled = scaler.transform(X_test)
    X_test = pd.DataFrame(X_test_scaled)
    pred = model.predict(X_test)
    return(pred)
