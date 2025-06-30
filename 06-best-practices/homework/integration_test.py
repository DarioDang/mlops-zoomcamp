import pandas as pd 
from datetime import datetime 
import os 

# Run batch script
os.system("python batch.py 2023 1")

# Read the result from S3
s3_endpoint_url = os.getenv("S3_ENDPOINT_URL", "http://localhost:4566")
output_file = "s3://nyc-duration/out/2023-01.parquet"

options = {
    'client_kwargs': {
        'endpoint_url': s3_endpoint_url
    }
}

df_result = pd.read_parquet(output_file, storage_options=options)

print(df_result)
print("Sum of predicted durations:", df_result['predicted_duration'].sum())