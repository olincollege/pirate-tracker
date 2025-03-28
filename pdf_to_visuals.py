"""
Pirate Incident Map Plotter

This script reads pirate incident data from a CSV file, converts coordinates
from DMS (degrees, minutes, seconds) format to decimal, and plots them on
world and Southeast Asia maps.

Uses:
    - pandas: for reading CSV files
    - regex: for parsing DMS coordinates
    - shapely and geopandas: for mapping and plotting points
    - geodatasets: for world map data
    - matplotlib: for plotting

Functions:
    - sorting_into_df(csv): gets data from the CSV
    - dms_to_decimal_coordinates(lat_list, long_list): converts DMS to decimal
    - plotting_incidents_map(points): plots coordinates on maps
"""

import pandas as pd
import regex as re
from shapely.geometry import Point
import geopandas as gpd
from geopandas import GeoDataFrame
import geodatasets
import matplotlib.pyplot as plt


def sorting_into_df(csv):
    """
    Given a CSV file, seperates the given information into seperate

    Libraries:

        Pandas -> Allows us to read from CSV and create lists from...
        dataframes of sorted data (Index, ..., Description)

    ARGS:

        CSV - The given CSV file that we are parsing.

    Returns:

        This function returns the independent lists (index, ..., description).
    """

    df = pd.read_csv(csv)
    index_list = df["Index"].tolist()
    latitude_list = df["Latitude"].tolist()
    longitude_list = df["Longitude"].tolist()
    area_list = df["Area Location"].tolist()
    return index_list, latitude_list, longitude_list, area_list


def dms_to_decimal_coordinates(latitude_list, longitude_list):
    """
    Given coordinates in DMS format
    (degrees, minutes, seconds) for locations, convert to...
    longitude and latitude coordinate points.

    Libraries:

        Regex -> Allows us to look at the format of our DMS values and...
        extrapolate the given

    ARGS:

        latitude_list - A list containing latitude values in DMS format.
        longitude_list - A list containing longitude values in DMS format.

    Returns:

        A list containing coordinate points
        (tuples) of latitude and longitude values.
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
    print(coordinate_points)
    return coordinate_points


def plotting_incidents_map(coordinate_points):
    """
    Given a list of tuples (coordinate points),
    plot the coordinate points over...
    over the world map for visualization.

    Libraries used:

        Geopandas -> Converts coordinate points into
        geographic dataframe and loads world map data.

        Shapely -> Transforms lat/long pairs into plottable points.

        Matplotlib.pyplot -> Renders the final map visualization.

        Geodatasets -> Provides pre-loaded world map base layer.

    ARGS:

        coordinate_points - A list of coordinate points (lat, long).

    Returns:

        An image with an overlaying heatmap.

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
