import pdfplumber
import pandas as pd
import re

def extract_text_from_pdf(pdf_path):
    text_blocks = []
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            text_blocks.append(page.extract_text())
    return "\n".join(text_blocks)

def parse_incident_block(block):
    data = {}

    lines = block.splitlines()
    data["Ship Name"] = lines[0].strip() if lines else ""

    # Incident Type
    match = re.search(r'(Robbery ?/ ?Theft|Attempted)', block)
    data["Incident Type"] = match.group(1) if match else None

    # Date and Time
    date_match = re.search(r'(\d{1,2} \w+ \d{4})', block)
    time_match = re.search(r'(\d{4}|\d{2}:\d{2})', block)
    data["Date"] = date_match.group(1) if date_match else None
    data["Time"] = time_match.group(1) if time_match else None

    # Latitude and Longitude
    lat_match = re.search(r'(\d+°\s?\d+\.?\d*\'?\s?[NS])', block)
    long_match = re.search(r'(\d+°\s?\d+\.?\d*\'?\s?[EW])', block)
    data["Latitude"] = lat_match.group(1) if lat_match else None
    data["Longitude"] = long_match.group(1) if long_match else None

    # Flag of Ship and Type of Ship
    flag_type_match = re.search(r'\n([A-Z\s,]+)\s+([A-Z/ ]+SHIP|TANKER|CARRIER|VESSEL)', block)
    if flag_type_match:
        data["Flag of Ship"] = flag_type_match.group(1).strip()
        data["Type of Ship"] = flag_type_match.group(2).strip()
    else:
        data["Flag of Ship"] = None
        data["Type of Ship"] = None

    # Ship Activity
    activity_match = re.search(r'(At Anchor|At Berth|While Sailing)', block)
    data["Ship Activity"] = activity_match.group(1) if activity_match else None

    # Category (CAT)
    cat_match = re.search(r'\n([1-4]|NA)\s*$', block.strip())
    data["CAT"] = cat_match.group(1) if cat_match else None

    # Attack Description
    desc_match = re.search(r'Attack method & description of incident(.*?)\n(?:[1-4]|NA)\s*$', block, re.DOTALL)
    if desc_match:
        desc_text = desc_match.group(1).strip().replace('\n', ' ')
        data["Attack Description"] = re.sub(r'\s+', ' ', desc_text)
    else:
        data["Attack Description"] = None

    return data

def parse_pdf_to_dataframe(pdf_path):
    full_text = extract_text_from_pdf(pdf_path)
    incident_blocks = re.split(r'\n\d+\.\s+', full_text)[1:]  # Skip any header
    parsed_data = [parse_incident_block(block) for block in incident_blocks]
    return pd.DataFrame(parsed_data)

# Run the parser
pdf_path = "/Users/hongyizhang/Downloads/Pirate_Incidents_2024.pdf" #replace with your path of pdf
df = parse_pdf_to_dataframe(pdf_path)

df.to_csv("parsed_pirate_incidents.csv", index=False)

