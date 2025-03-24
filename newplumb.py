import pdfplumber
import json

# Path to your PDF file
pdf_path = "/mnt/c/Users/sbloom/Downloads/Pirate_Incidents_2024.pdf"
output_file = "pirate_incidents_parsed.json"  # Output file path

# Function to parse the table data and map it to the correct columns
def parse_table_data(table_data):
    # Create a dictionary to hold all the data
    data = {
        "S/N": [],
        "Name of ship": [],
        "Incident Type": [],
        "Flag of ship": [],
        "Ship Activity": [],
        "Attack Method & Description": []
    }

    # Initialize variables for processing attack descriptions
    attack_description = ""
    collecting_attack_description = False
    
    # Loop through each row in the table (skipping headers if present)
    for row in table_data[1:]:  # Skipping the first row (header row)
        if row:
            try:
                # Extract values based on their column index
                sn = row[0] if len(row) > 0 and row[0] != "" else None
                name_of_ship = row[1] if len(row) > 1 and row[1] != "" else None
                incident_type = row[2] if len(row) > 2 and row[2] != "" else None
                flag_of_ship = row[5] if len(row) > 5 and row[5] != "" else None
                ship_activity_raw = row[11] if len(row) > 11 and row[11] != "" else None
                ship_activity = None

                # Map Ship Activity to "While Sailing" or "At Anchor"
                if ship_activity_raw:
                    if "Sailing" in ship_activity_raw:
                        ship_activity = "While Sailing"
                    elif "Anchor" in ship_activity_raw:
                        ship_activity = "At Anchor"

                # Attack Method/Description logic (collect all text until a new "S/N" number)
                attack_method = row[12] if len(row) > 12 and row[12] != "" else None

                # Check if we need to start a new row and reset the attack description
                test_values = list(range(1, 107))
                for i in test_values:
                    if sn and sn.startswith(test_values(i) + "."):  # Indicates a new incident row starts
                        # If collecting, finalize the previous attack description
                        if collecting_attack_description:
                            data["Attack Method & Description"].append(attack_description.strip())
                            collecting_attack_description = False

                        # Start a new attack description
                        attack_description = attack_method if attack_method else ""
                        collecting_attack_description = True

                    else:
                        # Continue collecting attack descriptions
                        if collecting_attack_description and attack_method:
                            attack_description += " " + attack_method

                # Only append non-empty values to the lists
                if sn:
                    data["S/N"].append(sn)
                if name_of_ship:
                    data["Name of ship"].append(name_of_ship.replace("\n", " "))  # Clean up multiline values
                if incident_type:
                    data["Incident Type"].append(incident_type)
                if flag_of_ship:
                    data["Flag of ship"].append(flag_of_ship)
                if ship_activity:
                    data["Ship Activity"].append(ship_activity)

            except IndexError as e:
                print(f"Error processing row: {row}, {e}")
                continue

    # Append the final attack description if any
    if collecting_attack_description:
        data["Attack Method & Description"].append(attack_description.strip())

    return data

# Function to extract the table from the PDF
def extract_table_from_pdf(pdf_path):
    with pdfplumber.open(pdf_path) as pdf:
        first_page = pdf.pages[0]
        table = first_page.extract_table()
        return table

# Main function to drive the process
if __name__ == "__main__":
    # Extract table from PDF
    table = extract_table_from_pdf(pdf_path)

    # Parse the table data into structured format
    data = parse_table_data(table)

    # Save the parsed data to a JSON file
    with open(output_file, "w") as json_file:
        json.dump(data, json_file, indent=4)

    print(f"Data successfully saved to {output_file}")
