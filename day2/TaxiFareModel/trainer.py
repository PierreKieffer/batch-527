#!/usr/bin/env python3

import time
import json

import mlflow
from mlflow.tracking import MlflowClient
import joblib
import pandas as pd
from TaxiFareModel.data import get_data, clean_df, DIST_ARGS
from TaxiFareModel.encoders import TimeFeaturesEncoder, DistanceTransformer, AddGeohash, Direction, \
    DistanceToCenter
from TaxiFareModel.utils import compute_rmse, log
from memoized_property import memoized_property
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import GradientBoostingRegressor, RandomForestRegressor
from sklearn.linear_model import Lasso, Ridge, LinearRegression
from sklearn.model_selection import train_test_split, RandomizedSearchCV
from sklearn.pipeline import Pipeline, make_pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from xgboost import XGBRegressor

class Trainer():  

    def __init__(self, X, y, **kwargs): 
        self.X = X
        self.y = y
        self.X_train, self.X_test, self.y_train, self.y_test= train_test_split(self.X, self.y,test_size=0.1)

        self.nrows = kwargs.get("nrows", 1000)
        self.estimator = kwargs.get("estimator", "Linear")
        self.distance_type = kwargs.get("distance_type", "euclidian")

        self.mlflow = kwargs.get("mlflow", False)
        self.mlflow_uri = kwargs.get("mlflow_uri", None)
        self.experiment_name = kwargs.get("experiment_name", None)

        if self.mlflow : 
            self.mlflow_log_param("nrows", nrows)
            self.mlflow_log_param("distance_type", distance_type)
            self.mlflow_log_param("estimator", estimator)

    def get_estimator(self): 
        if self.estimator == "Lasso" : 
            model = Lasso()
        elif self.estimator == "Ridge" : 
            model = Ridge()
        elif self.estimator == "GBM": 
            model = GradientBoostingRegressor()
        elif self.estimator == "Linear" : 
            model = LinearRegression()
        elif self.estimator == "RandomForest" : 
            model  = RandomForestRegressor()
        elif self.estimator == "xgboost" : 
            model = XGBRegressor(objective='reg:squarederror', n_jobs=-1, max_depth=10, learning_rate=0.05,gamma=3)
        else : 
            model = Lasso()

        return model 

    def set_pipeline(self): 

        pipe_time_feature = make_pipeline(TimeFeaturesEncoder(time_column="pickup_datetime"), OneHotEncoder())
        pipe_distance = make_pipeline(DistanceTransformer(distance_type=self.distance_type, **DIST_ARGS ))

        features_encoder = ColumnTransformer(
                [
                    ("distance_feature", pipe_distance, list(DIST_ARGS.values())),
                    ("time_feature", pipe_time_feature, ["pickup_datetime"])
                    ]
                )

        self.pipeline = Pipeline(
                steps = [
                    ("features_encoder", features_encoder),
                    ("model", self.get_estimator())

                    ]
                )

    def train(self): 
        self.set_pipeline()
        self.pipeline.fit(self.X_train, self.y_train)

    def compute_rmse(self, X, y): 
        y_pred = self.pipeline.predict(X)
        rmse = compute_rmse(y_pred, y)
        return round(rmse, 3)

    def evaluate(self): 
        rmse_train = self.compute_rmse(self.X_train, self.y_train)
        rmse_test = self.compute_rmse(self.X_test, self.y_test)
        log("info", "rmse_train = {}".format(rmse_train))
        log("info", "rmse_test = {}".format(rmse_test))
        
        if self.mlflow : 
            self.mlflow_log_metric("rmse_train", rmse_train)
            self.mlflow_log_metric("rmse_test", rmse_test)


    ### MLFlow methods
    @memoized_property
    def mlflow_client(self):
        mlflow.set_tracking_uri(self.mlflow_uri)
        return MlflowClient()

    @memoized_property
    def mlflow_experiment_id(self):
        try:
            return self.mlflow_client.create_experiment(self.experiment_name)
        except BaseException:
            return self.mlflow_client.get_experiment_by_name(self.experiment_name).experiment_id

    @memoized_property
    def mlflow_run(self):
        return self.mlflow_client.create_run(self.mlflow_experiment_id)

    def mlflow_log_param(self, key, value):
        if self.mlflow:
            self.mlflow_client.log_param(self.mlflow_run.info.run_id, key, value)

    def mlflow_log_metric(self, key, value):
        if self.mlflow:
            self.mlflow_client.log_metric(self.mlflow_run.info.run_id, key, value)

    def log_estimator_params(self):
        reg = self.get_estimator()
        self.mlflow_log_param('estimator_name', reg.__class__.__name__)
        params = reg.get_params()
        for k, v in params.items():
            self.mlflow_log_param(k, v)

    def log_kwargs_params(self):
        if self.mlflow:
            for k, v in self.kwargs.items():
                self.mlflow_log_param(k, v)

    def log_machine_specs(self):
        cpus = multiprocessing.cpu_count()
        mem = virtual_memory()
        ram = int(mem.total / 1000000000)
        self.mlflow_log_param("ram", ram)
        self.mlflow_log_param("cpus", cpus)



if __name__=="__main__":

    param_set = [
            dict(
                nrows=1000,
                local=False,
                estimator="Linear",
                mlflow=True,
                distance_type="manhattan",
                mlflow_uri="http://localhost:5000",
                experiment_name="TaxiFareModel"
            ),
            dict(
                nrows=1000,
                local=False,
                estimator="Linear",
                mlflow=True,
                distance_type="haversine",
                mlflow_uri="http://localhost:5000",
                experiment_name="TaxiFareModel"
            ),
            dict(
                nrows=1000,
                local=False,
                estimator="RandomForest",
                mlflow=True,
                distance_type="manhattan",
                mlflow_uri="http://localhost:5000",
                experiment_name="TaxiFareModel"
            ),
            dict(
                nrows=1000,
                local=False,
                estimator="RandomForest",
                mlflow=True,
                distance_type="haversine",
                mlflow_uri="http://localhost:5000",
                experiment_name="TaxiFareModel"
            ),
            dict(
                nrows=1000,
                local=False,
                estimator="xgboost",
                mlflow=True,
                distance_type="haversine",
                mlflow_uri="http://localhost:5000",
                experiment_name="TaxiFareModel"
            ),
            ]

    for params in param_set : 

        '''
        INPUT PARAMS : 
        '''
        print(json.dumps(params, indent = 2))

        '''
        Load data
        '''
        log("info", "Load data")
        df = get_data(**params)
        df = clean_df(df)

        X = df.drop("fare_amount", axis =1)
        y = df["fare_amount"]

        '''
        Train
        '''
        log("info", "Train")
        trainer = Trainer(X, y, **params)
        trainer.train()

        '''
        Evaluate
        '''
        log("info", "Evaluate")
        trainer.evaluate()







