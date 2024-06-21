import pandas as pd
import numpy as np
import os

# Read the CSV file into a DataFrame
df = pd.read_csv('Location_1.csv')

# Define frequency bins and group the frequencies into these bins
start = 470
end = 862
step = 8
bins = list(range(start, end + step, step))
df['Frequency_bin'] = pd.cut(df['Frequency'], bins, right=False)

# Create a dictionary to name each channel and sort by the left bound of the interval
sorted_intervals = sorted(df['Frequency_bin'].dropna().unique(), key=lambda x: x.left)
name_dict = {interval: f"Channel_{i+1}_{interval.left}_to_{interval.right}"
             for i, interval in enumerate(sorted_intervals)}
df['Channel'] = df['Frequency_bin'].map(name_dict)

# Create a copy of the DataFrame for transformation
df1 = df.copy()

# Round the amplitude values and convert to string
for col in ['Amplitude']:
    df1[col] = df1[col].round(8).astype(str)

# Create a unique location identifier
df1['unique_loc'] = df1['Amplitude']

# Group by unique location and channel, and get the maximum amplitude
df1 = df1.groupby(['unique_loc', 'Channel'], observed=True)['Amplitude'].max().reset_index()

# Split the unique_loc back into amplitude
df1[['Amplitude']]  = df1['unique_loc'].apply(lambda x: pd.Series(x.split('--')))
del df1['unique_loc']

# Sort the DataFrame by channel name
df1['Channel_sort_key'] = df1['Channel'].apply(lambda x: int(x.split('_')[1]))
df1 = df1.sort_values('Channel_sort_key').drop(columns=['Channel_sort_key'])

# Create the directory for plots if it does not exist
if not os.path.exists('plots'):
    os.makedirs('plots')

# Save the transformed DataFrame to a CSV file
df1.to_csv('Location_1_channel_data.csv', index=False)


