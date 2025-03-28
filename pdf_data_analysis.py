"""
PDF Data Analysis Tool for Pirate Incidents

This script extracts coordinates, descriptions, and contextual phrases from
pirate attack reports in PDF format. Outputs include CSVs and text files.
"""

import re
import fitz  # PyMuPDF
import pandas as pd


def extract_pirate_locations(pdf_path, output_csv):
    """
    Extracts latitude, longitude, and area location
    for each pirate incident from a PDF report.

    Libraries:
        re -> Used to analyze text structure in the PDF.
        fitz -> Used to extract text from PDF files.
        pandas -> Used to store and process extracted data in DataFrames.

    ARGS:
        pdf_path (str): Path to the pirate tracker PDF file.
        output_csv (str): Path to the output CSV file to save extracted data.

    Returns:
        A dataFrame containing incident index, latitude,
        longitude, and area location, also saved to a CSV file.
    """
    doc = fitz.open(pdf_path)
    full_text = "".join(page.get_text() for page in doc)

    incident_blocks = re.findall(
        r"(\d+\.\s+.*?)(?=\n\d+\.\s+|\Z)", full_text, re.DOTALL
    )
    lat_pattern = re.compile(r"(\d{1,2}°\s*\d+(?:\.\d+)?'\s*[NS])")
    lon_pattern = re.compile(r"(\d{1,3}°\s*\d+(?:\.\d+)?'\s*[EW])")

    def _parse_incident(block):
        index_match = re.match(r"(\d+)\.", block)
        lat_match = lat_pattern.search(block)
        lon_match = lon_pattern.search(block)
        area_location = None
        if lon_match:
            post_lon_text = block[lon_match.end() :].strip()
            area_location = post_lon_text.split("\n")[0]
        return {
            "Index": int(index_match.group(1)) if index_match else None,
            "Latitude": lat_match.group(1) if lat_match else None,
            "Longitude": lon_match.group(1) if lon_match else None,
            "Area Location": area_location,
        }

    data = [_parse_incident(block) for block in incident_blocks]

    df = pd.DataFrame(data)
    df.to_csv(output_csv, index=False)

    print(f"Extracted {len(df)} incidents with lat/lon/area to '{output_csv}'")
    return df


def area_counter(csv_path, keywords=None):
    """
    Loads a CSV file and counts the most common keywords
    found in the 'Area Location' column.

    Libraries:
        pandas -> Used to process and filter information from the CSV file.

    ARGS:
        csv_path (str): Path to the CSV file containing
        the 'Area Location' column.
        keywords (list, optional): List of keywords to
        search for (case-insensitive). Defaults to a predefined set.

    Returns:
        None: Prints the frequency of each
        keyword in the 'Area Location' column.
    """
    if keywords is None:
        keywords = [
            "straits of malacca",
            "indonesia",
            "philippines",
            "bangladesh",
            "vietnam",
            "south china sea",
            "india",
            "malaysia",
        ]

    df = pd.read_csv(csv_path)
    df["Area Location"] = df["Area Location"].fillna("").astype(str).str.lower()

    counts = {}
    for kw in keywords:
        mask = df["Area Location"].str.contains(
            rf"\b{kw.lower()}\b", regex=True
        )
        counts[kw] = mask.sum()

    print("Most common area keywords:\n")
    print(pd.Series(counts).sort_values(ascending=False))


def extract_incident_descriptions(pdf_path, output_file):
    """
    Extracts incident descriptions from a pirate
    attack PDF and writes them to a text file.

    Libraries:
        fitz -> Used to access and extract text from the PDF.
        re -> Used to analyze text structure and extract relevant descriptions.

    ARGS:
        pdf_path (str): Path to the PDF file containing pirate attack reports.
        output_file (str): Path to the output file where
        extracted descriptions will be saved.

    Returns:
        The number of descriptions extracted and saved to the file.
    """
    doc = fitz.open(pdf_path)
    full_text = "".join(page.get_text() for page in doc)

    description_pattern = re.compile(
        r"(While (?:.|\n)+?)(?:\n\s*(?:[1-5]|NA)\s*\n)",
        re.IGNORECASE,
    )

    descriptions = description_pattern.findall(full_text)
    descriptions_cleaned = [
        re.sub(r"\s+", " ", desc).strip() for desc in descriptions
    ]

    with open(output_file, "w", encoding="utf-8") as f:
        for i, desc in enumerate(descriptions_cleaned, 1):
            f.write(f"{i}. {desc}\n\n")

    print(f"Saved {len(descriptions_cleaned)} descriptions to '{output_file}'")


def extract_top_contextual_phrases(file_path):
    """
    Extracts the top contextual phrases from pirate incident descriptions.

    Libraries:
        re -> Used to analyze text structure and extract relevant phrases.

    ARGS:
        file_path (str): Path to the text file
        containing pirate attack descriptions.

    Returns:
        The top 20 most frequent contextual phrases.
    """
    keywords = {
        "hostage": [
            "tied",
            "hostage",
            "injured",
            "escaped",
            "locked",
            "crew",
            "abducted",
            "assaulted",
        ],
        "theft": ["stolen", "missing", "robbed", "took", "taken", "removed"],
        "spare_parts": ["spare", "parts", "engine", "equipment"],
    }
    context_words = [
        "not",
        "no",
        "nothing",
        "were",
        "was",
        "reported",
        "appeared",
        "accounted",
    ]
    with open(file_path, "r", encoding="utf-8") as f:
        text = f.read()

    incident_blocks = re.findall(
        r"\d+\.\s+(.*?)(?=\n\d+\.|\Z)", text, re.DOTALL
    )
    incident_blocks = [
        re.sub(r"[^\w\s]", "", block.lower()) for block in incident_blocks
    ]

    n = 5
    relevant_phrases = {}
    all_keywords = set(sum(keywords.values(), [])) | set(context_words)
    combined_keywords = (
        keywords["theft"] + keywords["spare_parts"] + keywords["hostage"]
    )

    def _update_phrases(block):
        words = block.split()
        for gram in zip(*[words[i:] for i in range(n)]):
            if set(gram) & all_keywords:
                if any(k in gram for k in combined_keywords):
                    gram_str = " ".join(gram)
                    relevant_phrases[gram_str] = (
                        relevant_phrases.get(gram_str, 0) + 1
                    )

    for block in incident_blocks:
        _update_phrases(block)

    sorted_phrases = sorted(
        relevant_phrases.items(), key=lambda x: x[1], reverse=True
    )

    print("\nTop 20 contextual phrases:")
    for phrase, count in sorted_phrases[:20]:
        print(f'"{phrase}": {count}')
