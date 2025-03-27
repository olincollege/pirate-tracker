import fitz  # PyMuPDF
import re
import pandas as pd


def extract_pirate_locations(pdf_path, output_csv):
    """
    Extracts latitude, longitude, and area location for each pirate incident from a PDF report.

    Args:
        pdf_path (str): Path to the pirate tracker PDF file.
        output_csv (str): Path to the output CSV file to save extracted data.

    Returns:
        pd.DataFrame: A DataFrame containing incident index, latitude, longitude, and area location.
    """
    doc = fitz.open(pdf_path)

    # Extract text from all pages
    full_text = ""
    for page in doc:
        full_text += page.get_text()

    # Split the text into chunks for each incident
    incident_blocks = re.findall(
        r"(\d+\.\s+.*?)(?=\n\d+\.\s+|\Z)", full_text, re.DOTALL
    )

    lat_pattern = re.compile(r"(\d{1,2}°\s*\d+(?:\.\d+)?'\s*[NS])")
    lon_pattern = re.compile(r"(\d{1,3}°\s*\d+(?:\.\d+)?'\s*[EW])")

    data = []
    for block in incident_blocks:
        index_match = re.match(r"(\d+)\.", block)
        lat_match = lat_pattern.search(block)
        lon_match = lon_pattern.search(block)

        # Try to find the line after the longitude
        area_location = None
        if lon_match:
            post_lon_text = block[lon_match.end() :]
            lines = post_lon_text.strip().split("\n")
            for line in lines:
                line = line.strip()
                if line:
                    area_location = line
                    break

        data.append(
            {
                "Index": int(index_match.group(1)) if index_match else None,
                "Latitude": lat_match.group(1) if lat_match else None,
                "Longitude": lon_match.group(1) if lon_match else None,
                "Area Location": area_location,
            }
        )

    df = pd.DataFrame(data)
    df.to_csv(output_csv, index=False)

    print(f"Extracted {len(df)} incidents with lat/lon/area to '{output_csv}'")
    return df
