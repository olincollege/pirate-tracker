import pandas as pd

# Load the renamed CSV
df = pd.read_csv("Lat_Long_Description.csv")

# Get the Index column as a list
index_list = df["Index"].tolist()

# Print it in the terminal
print(index_list)
