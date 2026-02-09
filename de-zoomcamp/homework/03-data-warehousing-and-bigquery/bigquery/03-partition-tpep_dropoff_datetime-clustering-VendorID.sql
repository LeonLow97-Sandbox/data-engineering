CREATE OR REPLACE TABLE `homework-3-486903.trips.yellow_trips_2024_optimized`
PARTITION BY DATE(tpep_dropoff_datetime)
CLUSTER BY VendorID AS
SELECT *
FROM `homework-3-486903.trips.yellow_trips_2024_materialized`;