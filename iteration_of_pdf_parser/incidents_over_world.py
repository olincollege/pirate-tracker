import pandas as pd
import regex as re
from shapely.geometry import Point
import geopandas as gpd
from geopandas import GeoDataFrame
import geodatasets
import matplotlib.pyplot as plt


def sorting_into_df(csv):
    """
    Given a CSV file, separates the given information into separate lists.

    Args:
        csv - The path to the CSV file.

    Returns:
        index_list, latitude_list, longitude_list, area_list
    """
    df = pd.read_csv(csv)
    index_list = df["Index"].tolist()
    latitude_list = df["Latitude"].tolist()
    longitude_list = df["Longitude"].tolist()
    area_list = df["Area Location"].tolist()
    return index_list, latitude_list, longitude_list, area_list


def dms_to_decimal_coordinates(latitude_list, longitude_list):
    """
    Converts DMS-format coordinates to decimal degree format.

    Args:
        latitude_list - List of latitude values like "1° 3.28' N"
        longitude_list - List of longitude values like "103° 40.27' E"

    Returns:
        List of (lat, lon) tuples in decimal format.
    """
    lat_decimal_values = []
    long_decimal_values = []

    for coord in latitude_list:
        if not isinstance(coord, str):
            continue
        match = re.match(r"(\d+)°\s*(\d+(?:\.\d+)?)'\s*([NS])", coord)
        if match:
            degrees, minutes, direction = match.groups()
            decimal_value = float(degrees) + float(minutes) / 60
            if direction == "S":
                decimal_value *= -1
            lat_decimal_values.append(decimal_value)

    for coord in longitude_list:
        if not isinstance(coord, str):
            continue
        match = re.match(r"(\d+)°\s*(\d+(?:\.\d+)?)'\s*([EW])", coord)
        if match:
            degrees, minutes, direction = match.groups()
            decimal_value = float(degrees) + float(minutes) / 60
            if direction == "W":
                decimal_value *= -1
            long_decimal_values.append(decimal_value)

    coordinate_points = list(zip(lat_decimal_values, long_decimal_values))
    print(f"✅ Extracted {len(coordinate_points)} coordinate points")
    return coordinate_points


def plotting_incidents_map(coordinate_points):
    """
    Plots coordinate points on a world map and a focused Southeast Asia map.

    Args:
        coordinate_points - A list of (lat, lon) tuples.
    """
    geometry = [Point(lon, lat) for lat, lon in coordinate_points]
    gdf = GeoDataFrame(geometry=geometry)
    world = gpd.read_file(geodatasets.data.naturalearth.land["url"])

    # Global Map
    _, ax = plt.subplots(figsize=(10, 6))
    world.plot(ax=ax, color="lightgrey")
    gdf.plot(ax=ax, marker="o", color="red", markersize=1)
    ax.set_title("Global Pirate Attacks", fontsize=14, fontweight="bold")
    plt.savefig("Global_Pirate_Attacks.png", bbox_inches="tight", pad_inches=0)

    # Southeast Asia Map
    _, ax = plt.subplots(figsize=(10, 6))
    world.plot(ax=ax, color="lightgrey")
    gdf.plot(ax=ax, marker="o", color="red", markersize=2)
    ax.set_xlim(gdf.total_bounds[[0, 2]])
    ax.set_ylim(gdf.total_bounds[[1, 3]])
    ax.set_title(
        "Pirate Attacks around Southeast Asia", fontsize=14, fontweight="bold"
    )
    plt.savefig(
        "Pirate_Attacks_Southeast_Asia.png", bbox_inches="tight", pad_inches=0
    )


# Run the full pipeline
index_list, latitude_list, longitude_list, area_list = sorting_into_df(
    "pirate_locations.csv"
)
decimal_coordinates_final = dms_to_decimal_coordinates(
    latitude_list, longitude_list
)
plotting_incidents_map(decimal_coordinates_final)
