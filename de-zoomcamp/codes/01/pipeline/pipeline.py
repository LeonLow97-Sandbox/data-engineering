import sys
import pandas as pd

print('arguments', sys.argv)

month = int(sys.argv[1])

df = pd.DataFrame({
    "day": [1, 2, 3],
    "num_users": [4, 5, 6],
})
df['month'] = month
df.to_parquet(f"output_{month}.parquet") # parquet is binary data, compared to csv, it's better for performance
print(df.head())

print(f'hello pipeline, month={month}')
