import pandas as pd
import psycopg
from datetime import datetime
from evidently.metrics import ColumnQuantileMetric
from evidently.report import Report

# Load March 2024 data
url = "https://d37ci6vzurychx.cloudfront.net/trip-data/green_tripdata_2024-03.parquet"
df = pd.read_parquet(url)

# Extract pickup date
df['pickup_date'] = pd.to_datetime(df['lpep_pickup_datetime']).dt.date

# Collect daily median results
daily_medians = []

for day, day_df in df.groupby('pickup_date'):
    report = Report(metrics=[
        ColumnQuantileMetric(column_name="fare_amount", quantile=0.5)
    ])
    report.run(reference_data=day_df, current_data=day_df)

    result = report.as_dict()
    try:
        median = result['metrics'][0]['result']['current']['value']
        daily_medians.append((day, median))
    except KeyError:
        continue  # skip invalid days

# Create postgres_db if it doesn't exist
with psycopg.connect("host=localhost port=5433 user=postgres password=root", autocommit=True) as conn:
    res = conn.execute("SELECT 1 FROM pg_database WHERE datname = 'postgres_db'")
    if len(res.fetchall()) == 0:
        conn.execute("CREATE DATABASE postgres_db")

# Now connect to postgres_db and create table
with psycopg.connect("host=localhost port=5433 dbname=postgres_db user=postgres password=root", autocommit=True) as conn:
    with conn.cursor() as cur:
        # Create table
        cur.execute("""
        CREATE TABLE IF NOT EXISTS fare_metrics_2024 (
            pickup_date DATE PRIMARY KEY,
            median_fare FLOAT
        )
        """)

        # Insert daily metrics
        for day, median in daily_medians:
            cur.execute("""
                INSERT INTO fare_metrics_2024 (pickup_date, median_fare)
                VALUES (%s, %s)
                ON CONFLICT (pickup_date) DO UPDATE SET median_fare = EXCLUDED.median_fare
            """, (day, median))

print(" Median fare data saved to PostgreSQL (postgres_db).")
