1. Install DuckDB

```sh
# Create a python virtual environment
python3 -m venv .venv && source .venv/bin/activate

brew install duckdb
pip install duckdb
duckdb --version

pip install dbt-duckdb
dbt --version

pip install "dbt-core==1.7.14" "dbt-duckdb==1.7.2"

# initialise dbt project
dbt init taxi_rides_ny
```

2. Configure dbt profile

```yaml
# Update ~/.dbt/profiles.yml
taxi_rides_ny:
  target: dev
  outputs:
    # DuckDB Development profile
    dev:
      type: duckdb
      path: taxi_rides_ny.duckdb
      schema: dev
      threads: 1
      extensions:
        - parquet
      settings:
        memory_limit: '2GB'
        preserve_insertion_order: false

    # DuckDB Production profile
    prod:
      type: duckdb
      path: taxi_rides_ny.duckdb
      schema: prod
      threads: 1
      extensions:
        - parquet
      settings:
        memory_limit: '2GB'
        preserve_insertion_order: false

# Troubleshooting:
# - If you have less than 4GB RAM, try setting memory_limit to '1GB'
# - If you have 16GB+ RAM, you can increase to '4GB' for faster builds
# - Expected build time: 5-10 minutes on most systems
```

3. Ingest data

- Run `ingest.py` in `04/dbt-local/taxi_rides_ny/ingest.py`.

4. Launch DB UI

```
duckdb -ui
```

5. Test dbt connection

- Verify dbt can connect to your DuckDB database:

```
dbt debug
```

6. Install dbt Power User Extension (VS Code Users)
7. `dbt run`