#!/usr/bin/env python
# coding: utf-8


import pickle
import pandas as pd
import sys 

categorical = ['PULocationID', 'DOLocationID']

# Define function to read and prepare data
def read_data(filename):
    "Write a function to read and prepare data"
    df = pd.read_parquet(filename)
    df['duration'] = df.tpep_dropoff_datetime - df.tpep_pickup_datetime
    df['duration'] = df.duration.dt.total_seconds() / 60
    df = df[(df.duration >= 1) & (df.duration <= 60)].copy()
    df[categorical] = df[categorical].fillna(-1).astype('int').astype('str')
    return df


# Write a function to load the model and DictVectorizer
def load_model(model_path='model.bin'):
    "Write a function to load model and dv()"
    with open('model.bin', 'rb') as f_in:
        dv, model = pickle.load(f_in)
    return dv, model 

# Write a function to mmake predictions
def predict(df, dv, model):
    "Write a function to make a prediction"
    dicts = df[categorical].to_dict(orient='records')
    X_val = dv.transform(dicts)
    y_pred = model.predict(X_val)
    return y_pred 

# Build a result in DataFrame
def result_dataframe(df, y_pred, year, month):
    "Write a function to build a result DataFrame"
    # Create artificial ride_id
    df['ride_id'] = f'{year:04d}/{month:02d}_' + df.index.astype(str)
    # Build result dataframe
    df_result = pd.DataFrame()
    df_result['ride_id'] = df['ride_id']
    df_result['duration_prediction'] = y_pred
    return df_result


# Write the main pipeline function
def apply_model(input_file,output_file,year,month):
    "Write a function to run the model"
    print(f"Loading model...")
    dv, model = load_model()

    print(f"Reading data from {input_file}...")
    df = read_data(input_file)

    print("Making predictions...")
    y_pred = predict(df, dv, model)

    print(f"Prediction mean: {y_pred.mean():.2f}")

    print("Building result dataframe...")
    df_result = result_dataframe(df, y_pred, year, month)

    print(f"Saving results to {output_file}...")
    df_result.to_parquet(output_file, engine='pyarrow', compression=None, index=False)
    print("Done.")


# Write a run function
def run():
    "Write a function to execute the pipeline"
    taxi_type = sys.argv[1]  # 'yellow'
    year = int(sys.argv[2]) # 2023
    month = int(sys.argv[3]) # 4 
    input_file = f'https://d37ci6vzurychx.cloudfront.net/trip-data/{taxi_type}_tripdata_{year:04d}-{month:02d}.parquet'
    output_file = f'output/{taxi_type}_tripdata_{year:04d}-{month:02d}.parquet'

    apply_model(input_file=input_file, 
                output_file=output_file,
                year=year,
                month = month
    )

if __name__ == "__main__":
    run()

# To run the prediction: python [filename.py] [taxi_type] [year] [month]
    
# To run it in the Dockerfile use:
    # docker build --platform linux/amd64 -t homework-container .
    # docker run --rm -v $(pwd)/output:/app/output homework-container [taxi_type] [year] [month]















