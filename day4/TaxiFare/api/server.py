#!/usr/bin/env python3

from fastapi import FastAPI
import pandas as pd
import joblib

app = FastAPI()

@app.get("/predict")
def predict_handler(key, pickup_datetime, pickup_latitude,pickup_longitude, dropoff_latitude, dropoff_longitude, passenger_count): 

    '''
    get request data
    '''
    request_payload = {
            "key" : key, 
            "pickup_datetime" : pickup_datetime, 
            "pickup_longitude" : float(pickup_longitude), 
            "pickup_latitude" : float(pickup_latitude), 
            "dropoff_longitude" : float(dropoff_longitude), 
            "dropoff_latitude" : float(dropoff_latitude), 
            "passenger_count" : int(passenger_count)
            }

    '''
    format data to dataframe
    '''
    input_df = pd.DataFrame.from_dict([request_payload], orient = "columns")[["key", "pickup_datetime", "pickup_longitude", "pickup_latitude", "dropoff_longitude", "dropoff_latitude", "passenger_count"]]

    '''
    load model
    '''
    model = joblib.load("model.joblib")

    '''
    Predict
    '''
    prediction = model.predict(input_df)

    '''
    Build response payload 
    '''
    response_payload = {"prediction" : prediction[0]}

    return response_payload


