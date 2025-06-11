# Import library 
import pandas as pd
import datetime 
import time 
import random
import logging
import uuid 
import pytz
import io
import psycopg

# Set up logging option 
logging.basicConfig(level=logging.INFO, format= "%(asctime)s - [%(levelname)s]:  %(message)s")
SEND_TIMEOUT = 10
rand = random.Random()

# Create the table statement
create_table_statement = """
drop table if exists dummy_metrics;
create table dummy_metrics (
    timestamp timestamp,
    value1 integer,
    value2 varchar,
    value3 float
)
"""


# Def a function to stored database
def prep_db():
    "Write a function to configure the database"
    with psycopg.connect(" host=localhost port =5433 user=postgres password =root", autocommit=True) as conn:
        res = conn.execute("SELECT 1 FROM pg_database WHERE datname = 'postgres_db'")
        if len(res.fetchall()) == 0:
            conn.execute("CREATE DATABASE postgres_db")
        with psycopg.connect("host=localhost  port =5433 dbname =postgres_db user=postgres password =root") as conn:
            conn.execute(create_table_statement)


# Def function to calculate dummy metrics
def calculate_dummy_metrics_postgresql(curr):
    "Write a function to calculate dummy metrics"
    value1 = rand.randint(0, 100)
    value2 = str(uuid.uuid4())
    value3 = rand.random()

    curr.execute(
        "INSERT INTO dummy_metrics (timestamp, value1, value2, value3) VALUES (%s, %s, %s, %s)",
        (datetime.datetime.now(pytz.timezone('Pacific/Auckland')), value1, value2, value3)
    )

# Write a main function to insert timestamp values into the database
def main():
    "Write a main function with a for loop"
    prep_db()
    last_send = datetime.datetime.now() - datetime.timedelta(seconds=10)
    with psycopg.connect("host=localhost  port =5433 dbname =postgres_db user=postgres password =root", autocommit=True) as conn:
        for i in range(0,100):
            with conn.cursor() as curr:
                calculate_dummy_metrics_postgresql(curr)
            new_send = datetime.datetime.now()
            seconds_elapsed = (new_send - last_send).total_seconds()
            if seconds_elapsed <  SEND_TIMEOUT:
                time.sleep(SEND_TIMEOUT - seconds_elapsed)
            while last_send < new_send:
                last_send = last_send + datetime.timedelta(seconds=10)
            logging.info("data sent")

if __name__ == "__main__":
    main()
