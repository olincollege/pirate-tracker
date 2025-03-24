import PyPDF2
import json

def extract_text_from_pdf(pdf_path):
    with open(pdf_path, 'rb') as file:
        pdf_reader = PyPDF2.PdfReader(file)
        num_pages = len(pdf_reader.pages)
        full_text = ""
        
        # Extracting the text from each page.
        for page_num in range(num_pages):
            page = pdf_reader.pages[page_num]
            page_text = page.extract_text()
            full_text += page_text 
        return full_text
    
# Organizing the .txt file, such that the information is sorted into dictionaries
def organizing_incidents_text(incidents_text):
    columns = [
        "S/N", 
        "Name of ship",
        "Incident Type",
        "Date of incident",
        "Time of incident",
        "Flag of ship",
        "Type of ship",
        "Latitude",
        "Longitude",
        "Area location",
        "Area description",
        "Attack method & description of incident",
        "CAT"
    ]
    
    parsed_data = []
    
    # reformatting, such that we can place values into a dictionary.
    split_text = incidents_text.split("  ")  # Split based on double spaces
    split_text = [part.replace("\n", " ").strip() for part in split_text]

    for i in range(0, len(split_text), 13):
        row_data = {}
        current_row = split_text[i:i + 13]
        
        for j, part in enumerate(current_row):
            row_data[columns[j]] = part 
        
        parsed_data.append(row_data)
        
    return parsed_data

# Calling the function
PDF_PATH = "/mnt/c/Users/sbloom/Downloads/Pirate_Incidents_2024.pdf"
extracted_text = extract_text_from_pdf(PDF_PATH)

refromatted_incidents = organizing_incidents_text(extracted_text)

with open("parsed_pirate_incidents.json", "w", encoding="utf-8") as json_file:
        json.dump(refromatted_incidents, json_file, indent=4)
    
print("JSON file 'parsed_pirate_incidents.json' has been created.")
