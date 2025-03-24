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

# Example usage
PDF_PATH = "/mnt/c/Users/sbloom/Downloads/Pirate_Incidents_2024.pdf"
extracted_text = extract_text_from_pdf(PDF_PATH)
    
# Save the extracted text to a file
with open("PYPDF_extracted_text.txt", "w", encoding="utf-8") as text_file:
    text_file.write(extracted_text)
    print("Text extraction complete!")

# Organizing the .txt file, such that the information is sorted into dictionaries

