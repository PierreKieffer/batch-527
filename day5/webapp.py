#!/usr/bin/env python3

import streamlit as st
import numpy as np
import pandas as pd
from datetime import datetime
import requests
from PIL import Image 

landing_image = Image.open("taxi.png")
st.image(landing_image)
# st.markdown("""# Taxi Fare UPS (Ultra Prediction System )""")

date = datetime.utcnow().replace(microsecond=0)

date ="{} UTC".format(str(date))

pickup_datetime = st.text_input("pickup_datetime", str(date))
pickup_latitude = st.number_input("pickup_latitude", None)
pickup_longitude = st.number_input("pickup_longitude", None)
dropoff_latitude = st.number_input("dropoff_latitude", None)
dropoff_longitude = st.number_input("dropoff_longitude", None)
passenger_count = st.number_input("passenger_count", 1)


params = {
        "pickup_datetime" : pickup_datetime, 
        "pickup_latitude" : pickup_latitude, 
        "pickup_longitude" : pickup_longitude, 
        "dropoff_latitude" : dropoff_latitude, 
        "dropoff_longitude" : dropoff_longitude, 
        "key" : "key", 
        "passenger_count" : passenger_count
        }

if st.button('run prediction'):

    response = requests.get("https://taxifare-5ciz54dinq-ew.a.run.app/predict",  params = params)

    prediction = response.json().get("prediction", None)
    result = "taxi fare prediction : {} $".format(prediction)
    result






