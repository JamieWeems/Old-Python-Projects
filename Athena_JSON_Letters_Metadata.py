import os
import json
import csv
import logging

# Configure logging
logging.basicConfig(filename=r"log_file.log", level=logging.ERROR, format='%(asctime)s %(message)s')

print("Process has started!")

def extract_data_from_json(json_data):
    extracted_data = []
    # Ensure the JSON data contains an 'encounterdocuments' array
    encounterdocuments = json_data.get('letters', [])
    for i, doc in enumerate(encounterdocuments):
        try:
            # Extract specified data points, with defaults if they are missing
            createddate = doc.get('createddate', '')
            description = doc.get('description', '')
            documentclass = doc.get('documentclass', '')
            documentdescription = doc.get('documentdescription', '')
            encounterid = doc.get('encounterid', '')
            lastmodifieddate = doc.get('lastmodifieddate', '')
            letterid = doc.get('letterid', '')
            patientid = doc.get('patientid', '')
            extracted_data.append([createddate, description, documentclass, documentdescription, encounterid, lastmodifieddate, letterid, patientid])
        except Exception as e:
            logging.error(f"Error extracting data from document {i} in JSON: {e}")
            print(f"Error extracting data from document {i} in JSON: {e}")
    return extracted_data

def write_json_to_csv(json_directory, csv_file_path):
    # Open CSV file for writing
    try:
        with open(csv_file_path, 'w', newline='', encoding='utf-8') as csv_file:
            csv_writer = csv.writer(csv_file)
            # Write header
            csv_writer.writerow(['createddate', 'description', 'documentclass', 'documentdescription', 'encounterid', 'lastmodifieddate', 'letterid', 'patientid'])
            
            # Recursively search for 'EncounterDocument.json' files
            for root, dirs, files in os.walk(json_directory):
                for filename in files:
                    if filename == 'Letter.json':
                        file_path = os.path.join(root, filename)
                        print(f"Processing file: {file_path}")
                        try:
                            with open(file_path, 'r', encoding='utf-8') as json_file:
                                try:
                                    json_data = json.load(json_file)
                                    data_points = extract_data_from_json(json_data)
                                    if data_points:
                                        csv_writer.writerows(data_points)
                                        print(f"Extracted and wrote {len(data_points)} data points from {file_path}")
                                except json.JSONDecodeError as e:
                                    logging.error(f"Error decoding JSON from file {file_path}: {e}")
                                    print(f"Error decoding JSON from file {file_path}: {e}")
                        except Exception as e:
                            logging.error(f"Error reading file {file_path}: {e}")
                            print(f"Error reading file {file_path}: {e}")
    except Exception as e:
        logging.error(f"Error opening CSV file {csv_file_path} for writing: {e}")
        print(f"Error opening CSV file {csv_file_path} for writing: {e}")

if __name__ == "__main__":
    # Directory containing JSON files
    json_directory = r""

    # Path to the output CSV file
    csv_file_path = r""

    # Process JSON files and write to CSV
    write_json_to_csv(json_directory, csv_file_path)

    # Pause to review the results
    print("Processing complete!")
