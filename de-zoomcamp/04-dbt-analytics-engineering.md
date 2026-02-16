# dbt

## dbt Project Structure

When you launch dbt, a bunch of folders were created:

- `analyses`
  - A place for SQL files that you don't want to expose to stakeholders
  - Used for data quality reports
  - Lots of people don't use it.
- `dbt_project.yml`
  - Most important file in dbt.
  - Tell dbt some default, you need to run dbt commands.
  - For dbt core, your profile should match the one in the `.dbt/profiles.yml`.
- `macros`
  - They behave like Python functions (reusable logic)
  - They help to encapsulate logic in one place and are testable.
- `seeds`
  - Directory space to upload csv and flat files (to add them to dbt later)
  - Quick and dirty approach (better to fix at source)
- `snapshots`
  - Take a snapshot of a table at a moment in time.
  - Useful to track the history of a column that overwrites itself.
- `tests`
  - A place to put assertions in SQL format.
  - If this SQL command returns more than 0 rows, the dbt build fails.
- `models` (sql files)
  - dbt suggests 3 subfolders:
    - `staging`
      - Sources (raw table from database)
      - staging files that are 1 to 1 copy of your data with minimal cleaning steps.
        - Data types
        - Renaming columns
    - `intermediate`
      - Anything that is not raw nor you want to expose
      - No guidelines, just nice for heavy duty cleaning or complex logic
    - `marts`
      - If it is in marts, it is ready for consumption.
      - Tables ready for dashboards
      - Properly modeled, clean tables

## dbt Sources

## dbt Seed

- Add a seed file then run `dbt seed`

## dbt Tests

- Singular tests
- Source freshness (`dbt source freshness`)
- Generic tests
- Unit tests
- Model contracts

## dbt Documentation

- `dbt docs generate`
- `dbt docs serve`

## dbt Packages

- `dbt_expectations`

```yaml
packages:
  - package: dbt-labs/dbt_utils
    version: 1.3.3
```

- Run `dbt deps` to install dependencies.

## dbt Commands

- `dbt init`: build a dbt project, run once at the beginning, creates directories needed for the project.
- `dbt debug`: checks profiles.yml and see if there is a valid connection to database.
- `dbt seed`: ingests all csv files in `seeds` folder.
- `dbt snapshot`
- `dbt source freshness`: to find out if dbt data is stale.
- `dbt docs generate`
- `dbt docs serve`
- `dbt clean`
- `dbt compile`: takes dbt models and under `target/compiled`, places all codes directly sent to database (not jinja code).

Most command dbt commands:

- `dbt run`: takes every single model in dbt project and materializes it. Also tests if views can be created successfully.
- `dbt build`: `dbt run + dbt test + dbt seed + dbt snapshot` runs multiple dbt commands
  - `dbt retry`: continues building from which stage it failed.

Flags in dbt commands:

- `--help` or `-h`
- `--version`
- `-v`
- `dbt run --full-refresh`: underlying data has changed in incremental model, still want to perform a full refresh.
- `dbt run --fail-fast`: strict version of dbt run, fails even when there are warnings.
- `dbt run -t`: targets. by default it is `dev`
  - `dbt run -t prod`: target becomes `prod`
- `dbt run --select` or `dbt run -s`: specify one model
  - e.g., `dbt run --select stg_green_tripdata`
  - e.g., `dbt run --select int_trips_unioned`: run only this model.
  - e.g., `dbt run --select +int_trips_unioned`: added a `+` sign before to run everything that depends on this in the upstream.
  - e.g., `dbt run --select int_trips_unioned+`: added a `+` sign after to run everything in downstream dependencies.
  - e.g., `dbt run --select models/intermediate`
