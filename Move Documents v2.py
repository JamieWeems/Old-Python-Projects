import os
import shutil
import csv
import logging

def configure_logging(log_file_path):
    """
    Configures the logging settings.

    :param log_file_path: Path to the log file.
    """
    logging.basicConfig(filename=log_file_path, level=logging.INFO, format='%(asctime)s - %(message)s')

def move_document(src_file, dest_folder):
    """
    Moves a document to the designated folder, creating the folder if it does not exist.
    
    :param src_file: Path to the source file.
    :param dest_folder: Path to the destination folder.
    """
    try:
        # Check if source file exists
        if not os.path.isfile(src_file):
            print(f"Error: Source file '{src_file}' not found.")
            logging.info(f"Source file '{src_file}' not found.")
            return
        
        # Create the destination folder if it does not exist
        os.makedirs(dest_folder, exist_ok=True)
        
        # Move the file to the destination folder
        shutil.move(src_file, dest_folder)
        
        print(f"File {src_file} moved to {dest_folder} successfully.")
    except PermissionError:
        print(f"Error: Permission denied while moving '{src_file}' to '{dest_folder}'.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

def read_csv_and_move_documents(csv_file_path):
    """
    Reads the CSV file and moves each document to the designated folder.
    
    :param csv_file_path: Path to the CSV file.
    """
    try:
        with open(csv_file_path, newline='', encoding='utf-8') as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                if len(row) < 2:
                    print(f"Skipping invalid row: {row}")
                    continue
                
                src_file = row[0].strip()
                dest_folder = row[1].strip()
                print(f"Processing: Source='{src_file}' Destination='{dest_folder}'")
                move_document(src_file, dest_folder)
    except FileNotFoundError:
        print(f"Error: CSV file '{csv_file_path}' not found.")
    except PermissionError:
        print(f"Error: Permission denied while reading '{csv_file_path}'.")
    except Exception as e:
        print(f"An unexpected error occurred while processing the CSV file: {e}")

if __name__ == "__main__":
    # Path to the CSV file | Make Sure the file is saved in UTF-8 Encoding
    csv_file_path = r"H:\H800s\H822\DocumentTeam\H822_Naming_Issues_09262024.csv"
    
    # Path to the log file
    log_file_path = r"H:\H800s\H822\DocumentTeam\missing_files.log"
    
    # Configure logging
    configure_logging(log_file_path)
    
    # Process the CSV file and move documents
    read_csv_and_move_documents(csv_file_path)
