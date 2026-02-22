# Setup

```sh
# 1. Install Bruin CLI
curl -LsSf https://getbruin.com/install/cli | sh

# 2. Initialize zoomcamp template
bruin init zoomcamp my-pipeline
```

### Question 1. Bruin Pipeline Structure

In a Bruin project, what are the required files/directories?

**Explanation**:

- `.bruin.yml` file sits at the root to tell the CLI "this is a Bruin project".
- All `.py` and `.sql` live in `assets/` directory.
- `pipeline/` conatins `pipeline.yml` (which configures the pipeline) and `assets/` directory.
- See: https://getbruin.com/docs/bruin/getting-started/pipeline.html
    - "A pipeline is defined with a `pipeline.yml` file, and all the assets need to be under a folder called `assets` next to this file"

```
pipeline/
+ ├─ pipeline.yml
  └─ assets/
    ├─ some.asset.yml
    ├─ another.asset.py
    └─ yet_another.asset.sql
```

**Answer**: `.bruin.yml` and `pipeline/` with `pipeline.yml` and `assets/`

---

### Question 2. Materialization Strategies

You're building a pipeline that processes NYC taxi data organized by month based on `pickup_datetime`. Which incremental strategy is best for processing a specific interval period by deleting and inserting data for that time period?

**Explanation**:

- The `time_interval` strategy is designed for incrementally loading time-based data. It's useful when you want to process data within specific time windows, ensuring efficient updates of historical data while maintaining data consistency.
- This strategy requires the following configuration:
    - `incremental_key`: The column used for time-based filtering
    - `time_granularity`: Must be either 'date' or 'timestamp'
See: https://getbruin.com/docs/bruin/assets/materialization.html

**Answer**: `time_interval`

---

### Question 3. Pipeline Variables

You have the following variable defined in `pipeline.yml`:

```yaml
variables:
  taxi_types:
    type: array
    items:
      type: string
    default: ["yellow", "green"]
```

How do you override this when running the pipeline to only process yellow taxis?

**Explanation**: Bruin overrides pipeline variables using `--var`. For an array variable, you pass a JSON array (e.g., ["yellow"]).
See: https://getbruin.com/docs/bruin/core-concepts/variables.html

**Answer**: `bruin run --var 'taxi_types=["yellow"]'`

---

### Question 4. Running with Dependencies

You've modified the `ingestion/trips.py` asset and want to run it plus all downstream assets. Which command should you use?

**Explanation**:

- bruin run supports running a single asset by path, and `--downstream` runs all assets that depend on it.
- See: https://getbruin.com/docs/bruin/commands/run.html

**Answer**: `bruin run ingestion/trips.py --downstream`

---

### Question 5. Quality Checks

You want to ensure the `pickup_datetime` column in your trips table never has NULL values. Which quality check should you add to your asset definition?

**Explanation**:

- The `not_null` check verifies the column contains no NULL values.
- See: https://getbruin.com/docs/bruin/quality/available_checks.html#not-null

**Answer**: `name: not_null`

---

### Question 6. Lineage and Dependencies

After building your pipeline, you want to visualize the dependency graph between assets. Which Bruin command should you use?

**Explanation**:

- bruin lineage shows upstream and downstream dependencies for an asset (i.e., the dependency graph around it).
- See: https://getbruin.com/docs/bruin/commands/lineage.html

**Answer**: `bruin lineage`

---

### Question 7. First-Time Run

You're running a Bruin pipeline for the first time on a new DuckDB database. What flag should you use to ensure tables are created from scratch?

**Explanation**:

- `--full-refresh` forces a clean rebuild behavior (truncation / `drop+recreate` depending on materialization), which is what you want on a fresh DuckDB database.
- See: https://getbruin.com/docs/bruin/commands/run.html

**Answer**: `--full-refresh`
