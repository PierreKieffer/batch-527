#!/usr/bin/env python3
import json
import sys
import joblib

def predict(input_json_data):
    '''
    Simulate user input
    '''

    log("info", "run prediction on {}".format(input_json_data))

    '''
    '''
    model = joblib.load("model.joblib")

    '''
    Process input payload
    '''
    input_data = json.loads(input_json_data)
    input_df = pd.DataFrame.from_dict([input_data], orient = "columns")[["key", "pickup_datetime", "pickup_longitude", "pickup_latitude", "dropoff_longitude", "dropoff_latitude", "passenger_count"]]

    '''
    Prediction

    '''
    pred = model.predict(input_df)
    return pred[0]



if __name__=="__main__":
    pred = predict(sys.argv[1])
    print("taxifare prediction : {} $")


