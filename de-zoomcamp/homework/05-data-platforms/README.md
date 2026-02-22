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

- A standard Bruin project structure requires a root configuration file named `.bruin.yml`.
- `pipeline.yml`: configures the pipeline's name, schedule, default connection and start date.
- `pipeline/` directory contains `pipeline,yml` and an `assets/` directory where Python and SQL scripts live.

**Answer**: `.bruin.yml` and `pipeline/` with `pipeline.yml` and `assets/`

### Question 2. Materialization Strategies

You're building a pipeline that processes NYC taxi data organized by month based on `pickup_datetime`. Which incremental strategy is best for processing a specific interval period by deleting and inserting data for that time period?

**Explanation**:

