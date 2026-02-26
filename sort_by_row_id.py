import pandas as pd

# Read the CSV file
file_path = r'c:\Users\Dave Sisk\Repos\soft-relate-data\sample-data-messy_200.csv'
df = pd.read_csv(file_path)

# Sort by row_id
df_sorted = df.sort_values('row_id').reset_index(drop=True)

# Save back to file
df_sorted.to_csv(file_path, index=False)
print(f"File sorted by row_id and saved to {file_path}")
