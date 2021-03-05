#!/usr/bin/env python3
import requests



if __name__=="__main__":

    params = {
                    "dropoff_latitude":40.74383544921875,
                    "dropoff_longitude":-73.98143005371094,
                    "key":"2015-01-27 13:08:24.0000002",
                    "passenger_count":1,
                    "pickup_datetime":"2015-01-27 13:08:24 UTC",
                    "pickup_latitude":40.7638053894043,
                    "pickup_longitude":-73.97332000732422}

# response = requests.get("http://localhost:8080/predict", params = params)

    h = {
            "Authorization" : "passwd", 
            "Content-Type" : "application/json"
            }
    
    response = requests.get("https://taxifare-5ciz54dinq-ew.a.run.app/predict", headers = h,  params = params)

    print(response.status_code)

    print(response.json())

