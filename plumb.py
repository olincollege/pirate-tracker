import pdfplumber
import pandas as pd
import re

pdf_path = "/Users/hzhang/Downloads/Pirate_Tracker.pdf"


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
    match = re.search(r"(Robbery ?\ ?Theft|Attempted)", block)
    data["Incident Type"] = match.group(1) if match else None

    # flag, type of ship
    flag_type_match = re.search(
        r"\n([A-Z\s,]+)\s+([A-Z\ ]+SHIP|TANKER|CARRIER|VESSEL)", block
    )
    if flag_type_match:
        data["Flag of Ship"] = flag_type_match.group(1).strip()
        data["Type of Ship"] = flag_type_match.group(2).strip()
    else:
        data["Flag of Ship"] = None
        data["Type of Ship"] = None

    # ship activity
    activity_match = re.search(r"(At Anchor|At Berth|While Sailing)", block)
    data["Ship Activity"] = activity_match.group(1) if activity_match else None

    # attack description
    desc_match = re.search(
        r"Attack method & description of incident(.*?)\n(?:[1-4]|NA)\s*$",
        block,
        re.DOTALL,
    )
    if desc_match:
        desc_text = desc_match.group(1).strip().replace("\n", " ")
        data["Attack Description"] = re.sub(r"\s+", " ", desc_text)
    else:
        data["Attack Description"] = None

    return data


def parse_pdf_to_dataframe(pdf_path):
    full_text = extract_text_from_pdf(pdf_path)
    incident_blocks = re.split(r"\n\d+\.\s+", full_text)[1:]  # Skip any header
    parsed_data = [parse_incident_block(block) for block in incident_blocks]
    return pd.DataFrame(parsed_data)


pdf_path = r"C:/Users/hzhang/Downloads/Pirate_Tracker.pdf"
df = parse_pdf_to_dataframe(pdf_path)

df.to_csv("INPROGREESS_parsed_pirate_incidents.csv", index=False)
