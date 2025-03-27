import fitz  # PyMuPDF
import re
import pandas as pd

# Open the PDF
doc = fitz.open("Pirate_Tracker.pdf")

# Extract text from all pages
full_text = ""
for page in doc:
    full_text += page.get_text()

# Split the text into chunks for each incident (starts with a number and dot)
incident_blocks = re.findall(r"(\d+\.\s+.*?)(?=\n\d+\.\s+|\Z)", full_text, re.DOTALL)

# Pattern to match latitude, longitude, and area location (based on line order)
lat_pattern = re.compile(r"(\d{1,2}°\s*\d+(?:\.\d+)?'\s*[NS])")
lon_pattern = re.compile(r"(\d{1,3}°\s*\d+(?:\.\d+)?'\s*[EW])")
# Area Location comes after Longitude in the PDF, so we look for it as the next non-empty line

data = []
for block in incident_blocks:
    index_match = re.match(r"(\d+)\.", block)
    lat_match = lat_pattern.search(block)
    lon_match = lon_pattern.search(block)

    # Try to find the line after the longitude
    area_location = None
    if lon_match:
        post_lon_text = block[lon_match.end():]
        lines = post_lon_text.strip().split("\n")
        # Grab the first meaningful line after longitude
        for line in lines:
            line = line.strip()
            if line:
                area_location = line
                break

    data.append({
        "Index": int(index_match.group(1)) if index_match else None,
        "Latitude": lat_match.group(1) if lat_match else None,
        "Longitude": lon_match.group(1) if lon_match else None,
        "Area Location": area_location
    })

# Build DataFrame
df = pd.DataFrame(data)
df.to_csv("pirate_locations.csv", index=False)

print(f"✅ Extracted {len(df)} incidents with lat/lon/area to 'pirate_locations.csv'")
