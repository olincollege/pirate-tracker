
import pdfplumber

pdf_path = "/Users/hongyizhang/Downloads/Pirate_Incidents_2024.pdf"

with pdfplumber.open(pdf_path) as pdf:
    with open("pirate_incidents_raw.txt", "w", encoding="utf-8") as outfile:
        for page in pdf.pages:
            text = page.extract_text()
            if text:
                outfile.write(text + "\n")
