---
title: README
jupyter: python3
---

## Data Collection: PortWatch API

For this project, we used the **PortWatch API** to gather data about ports worldwide. The PortWatch API is a service provided by PortWatch to give detailed information on ports, including incidents, traffic, locations, and more.

We wrote a Python function to pull data from the PortWatch API. The API provides the data in JSON format, which we then saved to a file called `Ship_Data.json`. Refer to `port_watch_api_parser.py`.

The URL used in the code points to the PortWatch API, where it fetches the port data. Then, the data from the API is returned as JSON, which is a popular format for storing and exchanging data. The data is then saved to a file called `Ship_Data.json`.

If you want to learn more about how to use their API, you can check out the [ArcGIS REST API documentation](https://developers.arcgis.com/rest/services-reference/enterprise/query-feature-service-layer/).

## Requirements

Make sure to install all the required libraries from the `requirements.text` file below. By running the code below in the terminal, you should have all the required libraries to run this code. Make sure to also run the import function.

```{python}
pip install -r requirements.txt
```

## Overview of Repo

All of our functions are either in `pdf_data_analysis.py`, `pdf_to_visuals`, and `port_watch_api_parser.py`. We simply called the functions in our computational essay and also provided visuals.

If you want to download the Pirate_Tracker.pdf for yourself onto your own computer, head over to https://www.recaap.org/ and download the 2024 pdf on the left side. It is also located in the repository itself!

Make sure that all the neccesary libraries are installed correctly and you are in an updated enough anaconda base. For us, we used a anaconda base python version of 3.12.9!
