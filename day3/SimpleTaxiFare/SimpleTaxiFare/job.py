from google.cloud import storage
import pandas as pd
from sklearn import linear_model
import numpy as np
import joblib
import os

### GCP configuration - - - - - - - - - - - - - - - - - - -

# /!\ you should fill these according to your account

### GCP Project - - - - - - - - - - - - - - - - - - - - - -

# not required here

### GCP Storage - - - - - - - - - - - - - - - - - - - - - -

BUCKET_NAME = 'ml-bucket-pierrekieffer'

##### Data  - - - - - - - - - - - - - - - - - - - - - - - -

# train data file location
# /!\ here you need to decide if you are going to train using the provided and uploaded data/train_1k.csv sample file
# or if you want to use the full dataset (you need need to upload it first of course)
BUCKET_TRAIN_DATA_PATH = 'data/taxi-fare-train.csv'


##### Training  - - - - - - - - - - - - - - - - - - - - - -

# not required here

##### Model - - - - - - - - - - - - - - - - - - - - - - - -

# model folder name (will contain the folders for all trained model versions)
MODEL_NAME = 'taxifare'


# model version folder name (where the trained model.joblib file will be stored)
MODEL_VERSION = 'v1'

### GCP AI Platform - - - - - - - - - - - - - - - - - - - -

# not required here

### - - - - - - - - - - - - - - - - - - - - - - - - - - - -

os.environ["GOOGLE_APPLICATION_CREDENTIALS"]="/home/pierre/cred.json"

def get_data():
    """method to get the training data (or a portion of it) from google cloud bucket"""
    print("gs://{}/{}".format(BUCKET_NAME, BUCKET_TRAIN_DATA_PATH))
    df = pd.read_csv("gs://{}/{}".format(BUCKET_NAME, BUCKET_TRAIN_DATA_PATH), nrows=1000)
    return df


def compute_distance(df,
                     start_lat="pickup_latitude",
                     start_lon="pickup_longitude",
                     end_lat="dropoff_latitude",
                     end_lon="dropoff_longitude"):
    lat_1_rad, lon_1_rad = np.radians(df[start_lat].astype(float)), np.radians(df[start_lon].astype(float))
    lat_2_rad, lon_2_rad = np.radians(df[end_lat].astype(float)), np.radians(df[end_lon].astype(float))
    dlon = lon_2_rad - lon_1_rad
    dlat = lat_2_rad - lat_1_rad

    a = np.sin(dlat / 2.0) ** 2 + np.cos(lat_1_rad) * np.cos(lat_2_rad) * np.sin(dlon / 2.0) ** 2
    c = 2 * np.arcsin(np.sqrt(a))
    return 6371 * c


def preprocess(df):
    """method that pre-process the data"""
    df["distance"] = compute_distance(df)
    X_train = df[["distance"]]
    y_train = df["fare_amount"]
    return X_train, y_train


def train_model(X_train, y_train):
    """method that trains the model"""
    rgs = linear_model.Lasso(alpha=0.1)
    rgs.fit(X_train, y_train)
    print("trained model")
    return rgs


STORAGE_LOCATION = 'models/simpletaxifare/model.joblib'

def upload_model_to_gcp(joblib_path):

    client = storage.Client()

    bucket = client.bucket(BUCKET_NAME)

    blob = bucket.blob(STORAGE_LOCATION)

    blob.upload_from_filename(joblib_path)


def save_model(reg):
    """method that saves the model into a .joblib file and uploads it on Google Storage /models folder
    HINTS : use joblib library and google-cloud-storage"""

    # saving the trained model to disk is mandatory to then beeing able to upload it to storage
    # Implement here
    joblib.dump(reg, 'model.joblib')
    print("saved model.joblib locally")

    # Implement here
    upload_model_to_gcp("model.joblib")
    print("uploaded model.joblib to gcp cloud storage under \n => {}".format(STORAGE_LOCATION))


if __name__ == '__main__':
    # get training data from GCP bucket
    df = get_data()

    # preprocess data
    X_train, y_train = preprocess(df)

    # train model (locally if this file was called through the run_locally command
    # or on GCP if it was called through the gcp_submit_training, in which case
    # this package is uploaded to GCP before being executed)
    reg = train_model(X_train, y_train)

    # save trained model to GCP bucket (whether the training occured locally or on GCP)
    save_model(reg)
