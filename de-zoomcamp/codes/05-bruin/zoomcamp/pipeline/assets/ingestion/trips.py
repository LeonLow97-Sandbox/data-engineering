"""@bruin

# - Convention in this module: use an `ingestion.` schema for raw ingestion tables.
name: ingestion.trips

# Docs: https://getbruin.com/docs/bruin/assets/python
type: python

# Pick a Python image version (Bruin runs Python in isolated environments).
image: python:3.11

connection: duckdb-default

# Choose materialization (optional, but recommended).
# Bruin feature: Python materialization lets you return a DataFrame (or list[dict]) and Bruin loads it into your destination.
# This is usually the easiest way to build ingestion assets in Bruin.
# Alternative (advanced): you can skip Bruin Python materialization and write a "plain" Python asset that manually writes
# into DuckDB (or another destination) using your own client library and SQL. In that case:
# - you typically omit the `materialization:` block
# - you do NOT need a `materialize()` function; you just run Python code
# Docs: https://getbruin.com/docs/bruin/assets/python#materialization
materialization:
  # choose `table` or `view` (ingestion generally should be a table)
  type: table
  strategy: append

destination:
  dataset: ingestion

# Define output columns (names + types) for metadata, lineage, and quality checks.
# Tip: mark stable identifiers as `primary_key: true` if you plan to use `merge` later.
# Docs: https://getbruin.com/docs/bruin/assets/columns
columns:
  - name: pickup_datetime
    type: timestamp
    description: "When the meter was engaged"
  - name: dropoff_datetime
    type: timestamp
    description: "When the meter was disengaged"

@bruin"""
import os
import requests
import pandas as pd
from datetime import datetime
from dateutil.relativedelta import relativedelta
from io import BytesIO
import json

BASE_URL = "https://d37ci6vzurychx.cloudfront.net/trip-data/"

def month_range(start: datetime, end: datetime):
    current = start.replace(day=1)
    while current <= end:
        yield current
        current += relativedelta(months=1)

def materialize():
    start_date = datetime.fromisoformat(os.environ["BRUIN_START_DATE"])
    end_date = datetime.fromisoformat(os.environ["BRUIN_END_DATE"])
    vars_json = os.environ.get("BRUIN_VARS", "{}")
    taxi_types = json.loads(vars_json).get("taxi_types", ["yellow"])

    frames = []

    for taxi_type in taxi_types:
        for dt in month_range(start_date, end_date):
            file_name = f"{taxi_type}_tripdata_{dt.year}-{dt.month:02d}.parquet"
            url = BASE_URL + file_name

            response = requests.get(url)
            if response.status_code != 200:
                continue

            df = pd.read_parquet(BytesIO(response.content))
            df["taxi_type"] = taxi_type
            frames.append(df)

    if not frames:
        return pd.DataFrame()

    return pd.concat(frames, ignore_index=True)