# Import library 
import datetime
import time
import random
import logging 
import uuid
import pytz
import pandas as pd
import io
import psycopg
import joblib
from prefect import task, flow
from evidently import ColumnMapping
from evidently.report import Report
from evidently.metrics import ColumnDriftMetric, DatasetDriftMetric, DatasetMissingValuesMetric


SEND_TIMEOUT = 10
rand = random.Random()

categorical_variables = ['PULocationID', 'DOLocationID']
numerical_variables = ['passenger_count', 'fare_amount','total_amount','trip_distance']

# Create the table statement
create_table_statement = """
drop table if exists dummy_metrics;
create table dummy_metrics (
    timestamp timestamp,
    prediction_drift float,
    num_drifted_columns integer,
    share_missing_values float
)
"""

reference_data = pd.read_parquet("../data/reference.parquet")
reference_data['ehail_fee'] = reference_data['ehail_fee'].astype('float64')

with open('../models/lin_reg.bin', 'rb') as f_in:
   dv, model = joblib.load(f_in)

# Read the whole dataset 
raw_data = pd.read_parquet("../data/green_tripdata_2021-01.parquet")

begin = datetime.datetime(2021, 1, 1, 0, 0, 0)


column_mapping = ColumnMapping(
    prediction='duration_minutes',
    numerical_features=numerical_variables,
    categorical_features=categorical_variables,
    target=None
)

report = Report(metrics=[
    ColumnDriftMetric(column_name='duration_minutes'),
    DatasetDriftMetric(),
    DatasetMissingValuesMetric()
])

@task
# Def a function to stored database
def prep_db():
    "Write a function to configure the database"
    with psycopg.connect(" host=localhost port =5433 user=postgres password =root", autocommit=True) as conn:
        res = conn.execute("SELECT 1 FROM pg_database WHERE datname = 'test_db'")
        if len(res.fetchall()) == 0:
            conn.execute("CREATE DATABASE test_db")
        with psycopg.connect("host=localhost  port =5433 dbname =test_db user=postgres password =root") as conn:
            conn.execute(create_table_statement)


# Def function to calculate dummy metrics

@task
def calculate_metrics_postgresql(i):
    current_data = raw_data[(raw_data.lpep_pickup_datetime >= (begin + datetime.timedelta(i))) &
                            (raw_data.lpep_pickup_datetime < (begin + datetime.timedelta(i + 1)))]

    if current_data.empty:
        logging.info(f"Day {i}: no data, skipped.")
        return

    current_data.fillna(0, inplace=True)
    current_data['ehail_fee'] = current_data['ehail_fee'].astype('float64')
    
    dicts = current_data[numerical_variables + categorical_variables].to_dict(orient='records')
    X = dv.transform(dicts)
    current_data['duration_minutes'] = model.predict(X)

    report.run(reference_data=reference_data, current_data=current_data, column_mapping=column_mapping)

    result = report.as_dict()
    prediction_drift = result['metrics'][0]['result']['drift_score']
    num_drifted_columns = result['metrics'][1]['result']['number_of_drifted_columns']
    share_missing_values = result['metrics'][2]['result']['current']['share_of_missing_values']

    with psycopg.connect("host=localhost port=5433 dbname=test_db user=postgres password=root", autocommit=True) as conn:
        with conn.cursor() as curr:
            curr.execute(
                "INSERT INTO dummy_metrics (timestamp, prediction_drift, num_drifted_columns, share_missing_values) "
                "VALUES (%s, %s, %s, %s)",
                (begin + datetime.timedelta(i), prediction_drift, num_drifted_columns, share_missing_values)
            )

    logging.info(f"Day {i}: data sent")


@flow
# Write a main function to insert timestamp values into the database
def batch_monitoring_backfill():
    prep_db()
    for i in range(31):
        calculate_metrics_postgresql(i)


        

if __name__ == '__main__':
    batch_monitoring_backfill()