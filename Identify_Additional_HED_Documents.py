import os
import csv
import shutil
from datetime import datetime

# Define paths
csv_file_path = r'path\to\your\csv_file.csv'  # Path to the CSV file containing document paths
destination_dir = r'path\to\destination\folder'  # Destination folder for matching documents
log_file_path = os.path.join(destination_dir, 'error_log.txt')  # Log file for errors
matching_file_log_path = os.path.join(destination_dir, 'matching_files_log.txt')  # Log file for matching files

# Create destination folder if it doesn't exist
os.makedirs(destination_dir, exist_ok=True)

# Function to check if document starts with U+0001 and U+00C0
def check_document_start(doc_path):
    try:
        with open(doc_path, 'rb') as file:
            # Read the first two bytes (characters) from the file
            first_two_bytes = file.read(2)

            # Unicode for U+0001 and U+00C0
            # U+0001 is \x01 in bytes, U+00C0 is \xC0 in bytes
            return first_two_bytes == b'\x01\xc0'

    except Exception as e:
        error_message = f"Error reading document {doc_path}: {e}"
        print(error_message)
        log_error(error_message)
        return False

# Function to copy a document to the destination directory
def copy_document(doc_path, destination_dir):
    try:
        file_name = os.path.basename(doc_path)
        destination_path = os.path.join(destination_dir, file_name)
        shutil.copy2(doc_path, destination_path)
        print(f"Copied document: {destination_path}")
        log_matching_file(f"Copied document: {destination_path}")

    except Exception as e:
        error_message = f"Error copying document {doc_path}: {e}"
        print(error_message)
        log_error(error_message)

# Function to log errors
def log_error(message):
    with open(log_file_path, 'a') as log_file:
        log_file.write(f"{datetime.now()} - {message}\n")

# Function to log successfully copied files
def log_matching_file(message):
    with open(matching_file_log_path, 'a') as log_file:
        log_file.write(f"{datetime.now()} - {message}\n")

# Function to process the CSV file and copy matching documents
def process_documents_from_csv(csv_file, destination_dir):
    try:
        with open(csv_file, newline='') as file:
            reader = csv.reader(file)
            for row in reader:
                doc_path = row[0].strip()  # Assuming the CSV has a single column with document paths

                if os.path.exists(doc_path):
                    if check_document_start(doc_path):
                        copy_document(doc_path, destination_dir)
                else:
                    error_message = f"File not found: {doc_path}"
                    print(error_message)
                    log_error(error_message)

    except Exception as e:
        error_message = f"Error reading CSV file: {e}"
        print(error_message)
        log_error(error_message)

# Run the script
process_documents_from_csv(csv_file_path, destination_dir)

print(f"Process completed. Check log file for errors: {log_file_path}")
print(f"Matching files logged at: {matching_file_log_path}")
