# Setup

```sh
# brew install uv

uv init --python 3.13.11
uv add pandas pyarrow
brew install libpq
brew link --force libpq
uv add --dev pgcli
uv add jupyter
uv add sqlalchemy

# Run PostgreSQL as a Docker container
docker network create pg-network
docker run -it --rm \
  -e POSTGRES_USER="root" \
  -e POSTGRES_PASSWORD="root" \
  -e POSTGRES_DB="ny_taxi" \
  -v ny_taxi_postgres_data:/var/lib/postgresql \
  -p 5432:5432 \
  --network pg-network \
  --name pg-database-network \
  postgres:18

uv run jupyter notebook

# Run PostgreSQL client
uv run pgcli -h localhost -p 5432 -u root -d ny_taxi

docker run -it \
  -e PGADMIN_DEFAULT_EMAIL="admin@admin.com" \
  -e PGADMIN_DEFAULT_PASSWORD="root" \
  -v pgadmin_data:/var/lib/pgadmin \
  -p 8085:80 \
  --network=pg-network \
  --name pgadmin \
  dpage/pgadmin4
```

# SQL Commands

## 2 Methods of JOINs

```sql
SELECT
	tpep_pickup_datetime,
	tpep_dropoff_datetime,
	total_amount,
	CONCAT(zpu."Borough", ' / ', zpu."Zone") AS "pickup_loc",
	CONCAT(zdo."Borough", ' / ', zdo."Zone") AS "dropoff_loc"
FROM 
	yellow_taxi_trips_2021_1 t,
	zones zpu,
	zones zdo
WHERE
	t."PULocationID" = zpu."LocationID" AND
	t."DOLocationID" = zdo."LocationID"
LIMIT 100;

SELECT
	tpep_pickup_datetime,
	tpep_dropoff_datetime,
	total_amount,
	CONCAT(zpu."Borough", ' / ', zpu."Zone") AS "pickup_loc",
	CONCAT(zdo."Borough", ' / ', zdo."Zone") AS "dropoff_loc"
FROM 
	yellow_taxi_trips_2021_1 t 
JOIN zones zpu
	ON t."PULocationID" = zpu."LocationID"
JOIN zones zdo
	ON t."DOLocationID" = zdo."LocationID"
LIMIT 100;
```

- Check if there are any drop off location or pick up location IDs that are not in yellow taxi trips table

```sql
SELECT
    COUNT(1)
FROM 
	yellow_taxi_trips_2021_1 t 
WHERE
	"DOLocationID" NOT IN (
		SELECT "LocationID" FROM zones
	)
    OR 
    "PULocationID" NOT IN (
        SELECT "LocationID" FROM zones
    );
```

- `LEFT JOIN`: includes all records from the left table (yellow_taxi_trips_2021_1), and the matched records from the right table (zones). The result is NULL from the right side, if there is no match.

```sql
SELECT
	tpep_pickup_datetime,
	tpep_dropoff_datetime,
	total_amount,
	CONCAT(zpu."Borough", ' / ', zpu."Zone") AS "pickup_loc",
	CONCAT(zdo."Borough", ' / ', zdo."Zone") AS "dropoff_loc"
FROM 
	yellow_taxi_trips_2021_1 t 
LEFT JOIN zones zpu
	ON t."PULocationID" = zpu."LocationID"
LEFT JOIN zones zdo
	ON t."DOLocationID" = zdo."LocationID"
LIMIT 100;
```

- `RIGHT JOIN`: includes all records from the right table (zones), and the matched records from the left table (yellow_taxi_trips_2021_1). The result is NULL from the left side, when there is no match.

```sql
SELECT
    tpep_pickup_datetime,
    tpep_dropoff_datetime,
    total_amount,
    CONCAT(zpu."Borough", ' / ', zpu."Zone") AS "pickup_loc",
    CONCAT(zdo."Borough", ' / ', zdo."Zone") AS "dropoff_loc"
FROM 
    yellow_taxi_trips_2021_1 t 
RIGHT JOIN zones zpu
    ON t."PULocationID" = zpu."LocationID"
RIGHT JOIN zones zdo
    ON t."DOLocationID" = zdo."LocationID"
LIMIT 100;
```

- `OUTER JOIN`: includes all records when there is a match in either left (yellow_taxi_trips_2021_1) or right (zones) table. 

```sql
SELECT
    tpep_pickup_datetime,
    tpep_dropoff_datetime,
    total_amount,
    CONCAT(zpu."Borough", ' / ', zpu."Zone") AS "pickup_loc",
    CONCAT(zdo."Borough", ' / ', zdo."Zone") AS "dropoff_loc"
FROM 
    yellow_taxi_trips_2021_1 t 
FULL OUTER JOIN zones zpu
    ON t."PULocationID" = zpu."LocationID"
FULL OUTER JOIN zones zdo
    ON t."DOLocationID" = zdo."LocationID"
LIMIT 100;
```

- `GROUP BY`: grouping by multiple columns.
- The following query groups by day and drop off location ID, counting the number of trips, maximum total amount, and maximum passenger count for each group.

```sql
SELECT
	CAST(tpep_dropoff_datetime AS DATE) AS "day",
	"DOLocationID",
	COUNT(1),
	MAX(total_amount),
	MAX(passenger_count)
FROM 
	yellow_taxi_trips_2021_1 t 
GROUP BY
	1, 2
ORDER BY 
	"day" ASC,
	"DOLocationID" ASC
;
```
