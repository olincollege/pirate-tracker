import fitz  # PyMuPDF
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
