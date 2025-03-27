import fitz  # PyMuPDF
import re

# Open the PDF
doc = fitz.open("Pirate_Tracker.pdf")

# Grab all text from the PDF
full_text = ""
for page in doc:
    full_text += page.get_text()

# Pattern to extract the description (starting with "While..." and ending before category)
description_pattern = re.compile(
    r"(While (?:at anchor|underway|sailing|at berth).*?)(?:\n\s*\d+\s*\n|\n\s*NA\s*\n)", re.DOTALL | re.IGNORECASE
)

# Find all matches
descriptions = description_pattern.findall(full_text)

# Clean up
descriptions_cleaned = [re.sub(r"\s+", " ", d).strip() for d in descriptions]

# Save to file
with open("incident_descriptions.txt", "w", encoding="utf-8") as f:
    for i, desc in enumerate(descriptions_cleaned, 1):
        f.write(f"{i}. {desc}\n\n")

print(f"Saved {len(descriptions_cleaned)} descriptions to 'incident_descriptions.txt'")
