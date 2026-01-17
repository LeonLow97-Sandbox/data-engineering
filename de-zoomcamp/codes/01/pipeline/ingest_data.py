#!/usr/bin/env python
# coding: utf-8

import click
import pandas as pd
from sqlalchemy import create_engine
from tqdm.auto import tqdm

dtype = {
    "VendorID": "Int64",
    "passenger_count": "Int64",
    "trip_distance": "float64",
    "RatecodeID": "Int64",
    "store_and_fwd_flag": "string",
    "PULocationID": "Int64",
    "DOLocationID": "Int64",
    "payment_type": "Int64",
    "fare_amount": "float64",
    "extra": "float64",
    "mta_tax": "float64",
    "tip_amount": "float64",
    "tolls_amount": "float64",
    "improvement_surcharge": "float64",
    "total_amount": "float64",
    "congestion_surcharge": "float64"
}

parse_dates = [
    "tpep_pickup_datetime",
    "tpep_dropoff_datetime"
]

@click.command()
@click.option('--user', default='root', help='Database user')
@click.option('--password', default='root', help='Database password')
@click.option('--host', default='localhost', help='Database host')
@click.option('--port', default=5432, type=int, help='Database port')
@click.option('--db', default='ny_taxi', help='Database name')
@click.option('--table', default='yellow_taxi_data', help='Target table name')
@click.option('--year', default=2021, type=int, help='Year of the data')
@click.option('--month', default=1, type=int, help='Month of the data')
@click.option('--chunksize', default=100000, type=int, help='Chunk size for processing')
def ingest_data(user, password, host, port, db, table, year, month, chunksize):
    """Ingest NYC taxi data into PostgreSQL database."""
    pg_user = user
    pg_pass = password
    pg_host = host
    pg_port = port
    pg_db = db
    target_table = table

    prefix = 'https://github.com/DataTalksClub/nyc-tlc-data/releases/download/yellow/'
    url = f'{prefix}yellow_tripdata_{year:04d}-{month:02d}.csv.gz'

    engine = create_engine(f'postgresql://{pg_user}:{pg_pass}@{pg_host}:{pg_port}/{pg_db}')

    df_iter = pd.read_csv(
        url,
        dtype=dtype,
        parse_dates=parse_dates,
        iterator=True,
        chunksize=100000,
    )

    # Inserting data in chunks
    first = True
    for df_chunk in tqdm(df_iter):
        if first:
            df_chunk.head(n=0).to_sql(
                name=target_table, 
                con=engine, 
                if_exists='replace'
            )
            first = False
        df_chunk.to_sql(
            name=target_table, 
            con=engine, 
            if_exists='append'
        )

if __name__ == '__main__':
    ingest_data()
