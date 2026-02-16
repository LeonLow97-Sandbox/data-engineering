select
    dispatching_base_num,
    CAST(pickup_datetime AS TIMESTAMP) as pickup_datetime,
    CAST(dropoff_datetime AS TIMESTAMP) as dropoff_datetime,
    PUlocationID  as pickup_location_id,
    DOlocationID  as dropoff_location_id,
from {{ source('raw', 'fhv_tripdata') }}
where dispatching_base_num is not null
  and CAST(pickup_datetime AS TIMESTAMP) >= '2019-01-01'
  and CAST(pickup_datetime AS TIMESTAMP) < '2020-01-01'
