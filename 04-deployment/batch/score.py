#!/usr/bin/env python
# coding: utf-8


import pickle 
import os 
import sys 
import pandas as pd 
import mlflow
import uuid 
from sklearn.feature_extraction import DictVectorizer 
from sklearn.ensemble import RandomForestRegressor 
from sklearn.metrics import mean_squared_error
from sklearn.metrics import root_mean_squared_error
from sklearn.pipeline import make_pipeline


# Create artificial ride_ids
def generate_uuids(n):
    "Write a function to generate artificial ride_ids"
    ride_ids = []
    for i in range(n):
        ride_ids.append(str(uuid.uuid4()))
    return ride_ids

# Read dataframe 
def read_dataframe(filename: str):
    "Write a function to read and processing dataframe"
    df = pd.read_parquet(filename)
    df['duration'] = df.lpep_dropoff_datetime - df.lpep_pickup_datetime
    df.duration = df.duration.dt.total_seconds() / 60
    df = df[(df.duration >= 1) & (df.duration <= 60)]
    df['ride_id'] = generate_uuids(len(df))
    return df

#   Prepare dictionaries for model input
def prepare_dictionaries(df: pd.DataFrame):
    "Write a function to combined features and prepared data"
    categorical = ['PULocationID', 'DOLocationID']
    df[categorical] = df[categorical].astype(str)
    df['PU_DO'] = df['PULocationID'] + '_' + df['DOLocationID']
    categorical = ['PU_DO']
    numerical = ['trip_distance']
    dicts = df[categorical + numerical].to_dict(orient='records')
    return dicts


# Load model from artifact
def load_model(run_id):
    "Write a function to load model from artifact"
    #logged_model = f'mlartifacts/1/{run_id}/artifacts/model'
    logged_model = f'../web-service-mlflow/mlartifacts/1/{run_id}/artifacts/model'
    model = mlflow.pyfunc.load_model(logged_model)
    return model

# Apply the model to the input data
def apply_model(input_file, run_id, output_file):
    "Write a function to run the model"
    print(f'Reading data from {input_file}...')
    df = read_dataframe(input_file)
    dicts = prepare_dictionaries(df)

    print(f'Loading the model with RUN_ID = {run_id}...')
    model = load_model(run_id)

    print('Applying the model...')
    y_pred = model.predict(dicts)
    print(f'Saving the result to {output_file}...')

    df_result = pd.DataFrame()
    df_result['ride_id'] = df['ride_id']
    df_result['lpep_pickup_datetime'] = df['lpep_pickup_datetime']
    df_result['PULocationID'] = df['PULocationID']
    df_result['DOLocationID'] = df['DOLocationID']
    df_result['actual_duration'] = df['duration']
    df_result['predicted_duration'] = y_pred
    df_result['diff'] = df_result['actual_duration'] - df_result['predicted_duration']
    df_result['model_version'] = run_id
    
    df_result.to_parquet(output_file, index=False)
    return df_result


# Run the model
def run():
    "Write a function to run the model"
    taxi_type =  sys.argv[1] # 'green'
    year = int(sys.argv[2]) #2021
    month = int(sys.argv[3]) # 3

    input_file = f'https://d37ci6vzurychx.cloudfront.net/trip-data/{taxi_type}_tripdata_{year:04d}-{month:02d}.parquet'
    output_file = f'output/{taxi_type}/{year:04d}-{month:02d}.parquet'

    # RUN_ID = '33d91be4d8184963b8648d4419ef6507' 
    run_id = sys.argv[4] # 33d91be4d8184963b8648d4419ef6507

    apply_model(input_file=input_file, 
                run_id=run_id, 
                output_file=output_file
    )

if __name__ == "__main__":
    run()






