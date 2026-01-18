## Question 1. Understanding Docker images

**Question**: Run docker with the `python:3.13` image. Use an entrypoint `bash` to interact with the container.

**Explanation**:

```sh
docker run -it --entrypoint=bash python:3.13
# Unable to find image 'python:3.13' locally
# 6a2920e3d16b: Download complete
# 5582010cab7f: Download complete
# 599d5b6b6766: Download complete
# 3fffeb567ed4: Download complete
# c9b629762372: Download complete
# 2470fab23101: Download complete
# 4a1c41792403: Download complete
# e4ae43d9b49b: Download complete

root@8017980a72b5:/# pip --version
# pip 25.3 from /usr/local/lib/python3.13/site-packages/pip (python 3.13)
```

**Answer**:

> The pip version in the image is `25.3`.

## Question 2. Understanding Docker networking and docker-compose

**Question**: Given the following `docker-compose.yaml`, what is the `hostname` and `port` that pgadmin should use to connect to the postgres database?

- Docker Compose File: /code/docker-compose.yaml

**Explanation**

- In Docker Compose, the containers / services are within the same network by default.
- Hostname:
  - Since both `db` and `pgadmin` services are on the same docker compose network, containers can reach each other by **service name** and **container name**.
  - Thus, `pgadmin` can connect to `db` service using hostname `db` or `postgres` (container name).
  - `localhost` is referring to the `pgadmin` container itself, so it won't work.
- Port:
  - The correct port is the **internal port** of the Postgres container, which is `5432` (not the mapped port `5433` on the host machine).
  - Because `pgadmin` is connecting from within the Docker network, it should use the internal port.
  - Thus, the correct port is `5432`.

**Test**: Ran `docker-compose up` and tested the connections from pgadmin, here are the results:

```sh
postgres:5433
# connection failed: connection to server at "10.89.0.5", port 5433 failed: Connection refused
# Is the server running on that host and accepting TCP/IP connections?

localhost:5432
# connection failed: connection to server at "127.0.0.1", port 5432 failed: Connection refused
# Is the server running on that host and accepting TCP/IP connections?

db:5433
# connection failed: connection to server at "10.89.0.5", port 5433 failed: Connection refused
# Is the server running on that host and accepting TCP/IP connections?

postgres:5432
# CONNECTED ✅

db:5432
# CONNECTED ✅
```

**Answer**:

> `postgres:5432` and `db:5432`

## Prepare data for Questions 3 ~ 6

```sh
# Fetch parquet data for green taxi trips in November 2025
wget https://d37ci6vzurychx.cloudfront.net/trip-data/green_tripdata_2025-11.parquet

# Fetch taxi zone lookup data
wget https://github.com/DataTalksClub/nyc-tlc-data/releases/download/misc/taxi_zone_lookup.csv

# Launch Postgres as a Docker Container
docker run -it --rm \
  -e POSTGRES_USER="root" \
  -e POSTGRES_PASSWORD="root" \
  -e POSTGRES_DB="homework" \
  -v homework_1_data:/var/lib/postgresql \
  -p 5450:5432 \
  postgres:18

# Launch a virtual environment in Python and install necessary packages
# brew install uv # if you don't have uv installed
uv init --python 3.14
uv add jupyter              # Install Jupyter
uv add --dev pgcli          # Install Dev dependencies
uv run jupyter notebook     # Launch Jupyter Notebook

# The jupyter notebook can be found in
# /code/homework.ipynb

# Launch pgcli to connect to Postgres
uv run pgcli -h localhost -p 5450 -u root -d homework

# Check that tables are created
# root@localhost:homework> \dt
# +--------+-------------+-------+-------+
# | Schema | Name        | Type  | Owner |
# |--------+-------------+-------+-------|
# | public | green_trips | table | root  |
# | public | zones       | table | root  |
# +--------+-------------+-------+-------+
# SELECT 2

# Check the number of records in each table
# root@localhost:homework> SELECT COUNT(1) FROM green_trips;
# +-------+
# | count |
# |-------|
# | 46912 |
# +-------+
# SELECT 1
# Time: 0.013s
# root@localhost:homework> SELECT COUNT(1) FROM zones;
# +-------+
# | count |
# |-------|
# | 265   |
# +-------+
# SELECT 1
# Time: 0.006s
```

## Question 3. Counting short trips

For the trips in November 2025 (lpep_pickup_datetime between '2025-11-01' and '2025-12-01', exclusive of the upper bound), how many trips had a `trip_distance` of less than or equal to 1 mile?

**Explanation**:

```sql
SELECT COUNT(1)
FROM green_trips
WHERE
    CAST(lpep_pickup_datetime AS DATE) >= '2025-11-01' AND
    CAST(lpep_pickup_datetime AS DATE) < '2025-12-01' AND
    trip_distance <= 1;
-- +-------+
-- | count |
-- |-------|
-- | 8007  |
-- +-------+
```

**Answer**:

> 8007

## Question 4. Longest trip for each day

Which was the pick up day with the longest trip distance? Only consider trips with `trip_distance` less than 100 miles (to exclude data errors).

**Explanation**:

```sql
SELECT
    CAST(lpep_pickup_datetime AS DATE) AS pickup_date,
    MAX(trip_distance) AS trip_distance
FROM
    green_trips
WHERE
    trip_distance < 100
GROUP BY
    1
ORDER BY
    trip_distance DESC
LIMIT 5
;
-- +-------------+---------------+
-- | pickup_date | trip_distance |
-- |-------------+---------------|
-- | 2025-11-14  | 88.03         |
-- | 2025-11-20  | 73.84         |
-- | 2025-11-23  | 45.26         |
-- | 2025-11-22  | 40.16         |
-- | 2025-11-15  | 39.81         |
-- +-------------+---------------+
```

**Answer**:

> 2025-11-14

## Question 5. Biggest pickup zone

Which was the pickup zone with the largest `total_amount` (sum of all trips) on November 18th, 2025?

**Explanation**:

```sql
SELECT
    z."Zone",
    SUM(total_amount) AS total_amount
FROM green_trips gt
JOIN zones z
    ON gt."PULocationID" = z."LocationID"
WHERE
    CAST(lpep_pickup_datetime AS DATE) = '2025-11-18'
GROUP BY
    z."Zone"
ORDER BY
    SUM(total_amount) DESC
LIMIT 5
;
-- +--------------------------+--------------------+
-- | Zone                     | total_amount       |
-- |--------------------------+--------------------|
-- | East Harlem North        | 9281.919999999991  |
-- | East Harlem South        | 6696.130000000004  |
-- | Central Park             | 2378.7899999999995 |
-- | Washington Heights South | 2139.05            |
-- | Morningside Heights      | 2100.5899999999992 |
-- +--------------------------+--------------------+
```

**Answer**:

> East Harlem North

## Question 6. Largest tip

For the passengers picked up in the zone named "East Harlem North" in November 2025, which was the drop off zone that had the largest tip?

**Explanation**:

```sql
SELECT
    z."Zone",
    gt.tip_amount
FROM green_trips gt
JOIN zones z
    ON gt."DOLocationID" = z."LocationID"
WHERE
    gt."PULocationID" = (
        SELECT "LocationID"
        FROM zones
        WHERE "Zone" = 'East Harlem North'
        LIMIT 1
    ) AND
    CAST(gt.lpep_pickup_datetime AS DATE) >= '2025-11-01' AND
    CAST(gt.lpep_pickup_datetime AS DATE) <= '2025-11-30' AND
    z."Zone" IS NOT NULL
ORDER BY
    gt.tip_amount DESC
LIMIT 5;

-- +-------------------------------+------------+
-- | Zone                          | tip_amount |
-- |-------------------------------+------------|
-- | Yorkville West                | 81.89      |
-- | LaGuardia Airport             | 50.0       |
-- | East Harlem North             | 45.0       |
-- | Long Island City/Queens Plaza | 34.25      |
-- | East Harlem North             | 26.0       |
-- +-------------------------------+------------+
```

**Answer**:

> Yorkville West

## Question 7. Terraform Workflow

Which of the following sequences, respectively, describes the workflow for:

1. Downloading the provider plugins and setting up backend,
2. Generating proposed changes and auto-executing the plan
3. Remove all resources managed by terraform

**Explanation**:

1. To download provider plugins to machine, we use `terraform init`.
2. To generate proposed changes and auto-execute plan, we use `terraform apply -auto-approve`.
  - Reading the docs, there is an `-auto-approve` flag in `terraform apply` command: https://developer.hashicorp.com/terraform/cli/commands/apply
  - What's NOT:
    - There is no `terraform plan -auto-apply`, docs: https://developer.hashicorp.com/terraform/cli/commands/plan
    - There is no `terraform run` command.
3. To remove all resources using Terraform, run `terraform destroy`.

**Answer**:

> terraform init --> terraform apply -auto-approve --> terraform destroy
