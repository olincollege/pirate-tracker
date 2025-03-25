import pandas as pd

df = pd.read_csv("Lat_Long_Description.csv")

# Get the Index column as a list
index_list = df["Index"].tolist()

# Get the Latitude column as a list
Latitude_list = df["Latitude"].tolist()

# Get the Longitude column as a list
Longitude_list = df["Longitude"].tolist()

# Get the Description column as a list
Description_list = df["Description"].tolist()

print(index_list)
