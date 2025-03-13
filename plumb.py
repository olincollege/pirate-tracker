import pdfplumber
import pandas as pd

def extract_incidents_from_pdf(pdf_path, output_csv="poop.csv"):
    rows = []

    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            text = page.extract_text()
            lines = text.split('\n')
            
            # look for lines starting with incident numbers like "1.", "2."
            current_entry = []
            for line in lines:
                if line.strip().startswith(tuple(str(i) + "." for i in range(1, 100))):
                    if current_entry:
                        rows.append("\n".join(current_entry))
                        current_entry = []
                current_entry.append(line)
            if current_entry:
                rows.append("\n".join(current_entry))  

    df = pd.DataFrame({"Incident Entry": rows})
    df.to_csv(output_csv, index=False)
    print(f"SAVED TO: {output_csv}")

    return df

path = "/Users/hongyizhang/Downloads/Pirate_Incidents_2024.pdf" #replace with your path of pdf
extract_incidents_from_pdf(path)
