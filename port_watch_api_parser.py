import json
import requests


def download_portwatch_data():
    """
    Fetches PortWatch port database JSON from a specific ArcGIS REST API endpoint
    and saves it to 'Ship_Data.json'.
    """
    api_url = "https://services9.arcgis.com/weJ1QsnbMYJlCHdG/arcgis/rest/services/PortWatch_ports_database/FeatureServer/0/query?where=1%3D1&outFields=*&outSR=4326&f=json"
    filename = "Ship_Data.json"

    response = requests.get(api_url, timeout=10)

    with open(filename, "w", encoding="utf-8") as file:
        file.write(response.text)


def extract_country_industries(jsonfile, outputfile):
    """
    Extracts and groups top industries by country from a JSON file containing port data,
    prints the result, and saves it to a file.

    Args:
        jsonfile: Path to the input JSON file.
        outputfile: Path to the output file for grouped data.

    Returns:
        A JSON file where each key is a country and the value is a list of unique industries
        mentioned across all its ports.
    """
    selected_countries = {
        "malacca",
        "indonesia",
        "bangladesh",
        "philippines",
        "vietnam",
        "china",
        "india",
    }

    with open(jsonfile, "r") as f:
        data = json.load(f)

    country_industries = {country: set() for country in selected_countries}

    for port in data.get("features", []):
        attrs = port.get("attributes", {})
        country = attrs.get("country", "").lower()
        if country in selected_countries:
            for key in ["industry_top1", "industry_top2", "industry_top3"]:
                industry = attrs.get(key)
                if industry:
                    country_industries[country].add(industry)

    country_industries = {
        country: sorted(list(industries))
        for country, industries in country_industries.items()
    }

    print("Extracted country industries:")
    for country, industries in country_industries.items():
        print(f"{country.title()}: {', '.join(industries)}")

    with open(outputfile, "w") as f_out:
        json.dump(country_industries, f_out, indent=4)
