import pdfplumber
import re
import pandas as pd


def extract_pdf_text(pdf_path):
    """
    Extract all text from a multi-page PDF using pdfplumber.
    
    Args:
        pdf_path: the path of the pdf you want to extract from
        
    Returns:
    
    """
    full_text = ""
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            full_text += page.extract_text() + "\n"
    return full_text


def clean_text(text):
    """Remove table headers and unwanted repeated blocks."""
    header_pattern = re.compile(
        r"S/N\s+Name of ship\s+Incident\s+Type\s+Date of\s+incident.*?(?=\d+\.\s)",
        re.DOTALL,
    )
    return header_pattern.sub("", text)


def parse_incidents(text):
    """Split incidents and extract index, lat, long, area, and full description."""
    raw_entries = re.split(r"\n(?=\d+\.\s)", text)

    data = []
    for entry in raw_entries:
        entry = entry.strip()
        if not entry:
            continue

        index_match = re.match(r"(\d+)\.", entry)
        lat_match = re.search(r"(\d{1,3}°\s[\d\.]+'\s[NS])", entry)
        lon_match = re.search(r"(\d{1,3}°\s[\d\.]+'\s[EW])", entry)

        # Match area between longitude and "While"
        area = None
        if lon_match:
            # Grab everything after longitude
            after_lon = entry[lon_match.end():]
            # Search for "While" and capture everything before it as area
            area_search = re.search(r"^(.*?)(?=While)", after_lon, re.DOTALL)
            if area_search:
                area = " ".join(area_search.group(1).split())

        desc_match = re.search(
            r"(While[\s\S]+?)(?:\n\s*\d{1,2}\s*$|\nCAT|\nS/N|$)", entry
        )

        if index_match and lat_match and lon_match and desc_match:
            index = int(index_match.group(1))
            lat = lat_match.group(1)
            lon = lon_match.group(1)

            # Clean up and normalize the paragraph
            desc_raw = desc_match.group(1)
            description = " ".join(desc_raw.splitlines()).strip()
            description = re.sub(r"\bWhile\s+While\b", "While", description)

            data.append(
                {
                    "Index": index,
                    "Latitude": lat,
                    "Longitude": lon,
                    "Area": area,
                    "Description": description,
                }
            )

    return pd.DataFrame(data)



pdf_path = "Pirate_Tracker.pdf"  # same directory
raw_text = extract_pdf_text(pdf_path)
cleaned_text = clean_text(raw_text)
df = parse_incidents(cleaned_text)

df.to_csv("lat_long_area_description.csv", index=False)
