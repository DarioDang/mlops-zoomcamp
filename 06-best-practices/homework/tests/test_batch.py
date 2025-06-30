import pandas as pd 
from datetime import datetime 
from batch import prepare_data 

def dt(hour, minute, second=0):
    return datetime(2023,1,1,hour,minute,second)

def test_prepare_data():
    data = [
        (None, None, dt(1,1), dt(1, 10)),           # duration = 9 mins (valid)
        (1, 1, dt(1, 2), dt(1, 10)),                # duration = 8 mins (valid)
        (1, None, dt(1, 2, 0), dt(1, 2, 59)),       # duration = 0.98 mins (too short)
        (3, 4, dt(1, 2, 0), dt(2, 2, 1)),           # duration = 1441 mins (too long)
    ]

    columns = ['PULocationID', 'DOLocationID', 'tpep_pickup_datetime', 'tpep_dropoff_datetime']
    df = pd.DataFrame(data, columns=columns)
    categorical = ['PULocationID', 'DOLocationID']
    actual_df = prepare_data(df, categorical)

    # Only the first two rows should remain  
    expected_data = [
        (-1, -1, 9.0),
        (1, 1, 8.0)
    ]
    expected_df = pd.DataFrame(expected_data, columns=['PULocationID', 'DOLocationID', 'duration'])
    expected_df[['PULocationID', 'DOLocationID']] = expected_df[['PULocationID', 'DOLocationID']].astype('int').astype('str')

    actual_result = actual_df[['PULocationID', 'DOLocationID', 'duration']].reset_index(drop=True)
    expected_result = expected_df.reset_index(drop=True)

    assert actual_result.equals(expected_result)