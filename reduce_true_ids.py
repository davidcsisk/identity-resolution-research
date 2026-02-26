import pandas as pd
import numpy as np

# Read the CSV file
file_path = r'c:\Users\Dave Sisk\Repos\soft-relate-data\sample-data-messy_200.csv'
df = pd.read_csv(file_path)

print(f"Original file: {len(df)} rows")
print(f"Unique true_ids: {df['true_id'].nunique()}")

# Randomly keep 2 out of 3 rows for each true_id
# Group by true_id and sample 2 rows from each group
df_reduced = df.groupby('true_id', as_index=False).apply(
    lambda x: x.sample(n=2, random_state=None)
).reset_index(drop=True)

print(f"Reduced file: {len(df_reduced)} rows")
print(f"Unique true_ids: {df_reduced['true_id'].nunique()}")

# Save the reduced file back to the same location
df_reduced.to_csv(file_path, index=False)
print(f"\nFile saved to {file_path}")
