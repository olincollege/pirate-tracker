import re
import fitz  # PyMuPDF
import pandas as pd


def extract_pirate_locations(pdf_path, output_csv):
    """
    Extracts latitude, longitude, and area location for each pirate incident from a PDF report.

    Libraries Accessed:

        regex -> used to analyze structure in the pdf.
        fitz -> used to open the file for further analysis.
        pandas -> sort the data into dataframes, upon which can be used.
        
    ARGS: 
    
        pdf_path (str): Path to the pirate tracker PDF file.
        output_csv (str): Path to the output CSV file to save extracted data.

    Returns:
    
        pd.DataFrame: A DataFrame containing incident index, latitude, longitude, and area location.
        
    """
    doc = fitz.open(pdf_path)

    # extract text
    full_text = ""
    for page in doc:
        full_text += page.get_text()

    # split the text into chunks for each incident
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


def area_counter(csv_path, keywords=None):
    """
    Load a CSV file and print the most common keywords found in the 'Area Location' column.

    Libraries Used:

        pandas -> used to process through the csv.
        
    Args:
        csv_path: Path to the CSV file containing the 'Area Location' column.
        keywords: Optional list of keywords to search for (case-insensitive).
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

# importing again.
import fitz
import re

def extract_incident_descriptions(pdf_path, output_file):
    """
    Extracts incident descriptions from a pirate attack PDF and writes them to a text file.

    Args:
        pdf_path (str): Path to the PDF file containing pirate attack reports.
        output_file (str): Path to the output text file where descriptions will be saved.

    Returns:
        int: The number of incident descriptions extracted and saved.
    """
    doc = fitz.open(pdf_path)

    full_text = ""
    for page in doc:
        full_text += page.get_text()

    description_pattern = re.compile(
        r"(While (?:.|\n)+?)(?:\n\s*(?:[1-5]|NA)\s*\n)",  # get rid of cat values (1-5 and N/A)
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
    return len(descriptions_cleaned)


import re


def extract_top_contextual_phrases(file_path):
    """
    qwer
    """
    # define core keywords by category
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

    # context words
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

    # split incidents
    incident_blocks = re.findall(
        r"\d+\.\s+(.*?)(?=\n\d+\.|\Z)", text, re.DOTALL
    )
    incident_blocks = [
        re.sub(r"[^\w\s]", "", block.lower()) for block in incident_blocks
    ]

    N = 5
    relevant_phrases = {}

    all_keywords = set(sum(keywords.values(), [])) | set(context_words)

    for block in incident_blocks:
        words = block.split()
        ngrams = zip(*[words[i:] for i in range(N)])

        for gram in ngrams:
            gram_set = set(gram)
            if gram_set & all_keywords:
                if any(
                    k in gram
                    for k in keywords["theft"]
                    + keywords["spare_parts"]
                    + keywords["hostage"]
                ):
                    gram_str = " ".join(gram)
                    if gram_str not in relevant_phrases:
                        relevant_phrases[gram_str] = 1
                    else:
                        relevant_phrases[gram_str] += 1

    # sorting by frequency (descending)
    sorted_phrases = list(relevant_phrases.items())
    for i in range(len(sorted_phrases)):
        for j in range(i + 1, len(sorted_phrases)):
            if sorted_phrases[j][1] > sorted_phrases[i][1]:
                sorted_phrases[i], sorted_phrases[j] = (
                    sorted_phrases[j],
                    sorted_phrases[i],
                )

    # top 20 phrases
    print("\nTop 20 contextual phrases:")
    for phrase, count in sorted_phrases[:20]:
        print(f'"{phrase}": {count}')
