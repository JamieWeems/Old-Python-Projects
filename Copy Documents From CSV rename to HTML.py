import os
import shutil
import csv
import logging

def setup_logging(log_file_path):
    logging.basicConfig(
        filename=log_file_path,
        level=logging.WARNING,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )

def copy_files_with_htm_extension(csv_file_path, log_file_path):
    setup_logging(log_file_path)

    try:
        with open(csv_file_path, mode='r', newline='') as csv_file:
            csv_reader = csv.reader(csv_file)
            header = next(csv_reader)  # Skip the header row

            for row in csv_reader:
                if len(row) != 2:
                    print(f"Skipping malformed row: {row}")
                    continue
                
                source_path = row[0]
                destination_path = row[1] 

                # Check if the source file exists
                if not os.path.exists(source_path):
                    print(f"Source file does not exist: {source_path}")
                    logging.warning(f"Source file does not exist: {source_path}")
                    continue

                # Create the destination directory if it does not exist
                destination_dir = os.path.dirname(destination_path)
                if not os.path.exists(destination_dir):
                    os.makedirs(destination_dir)
                
                # Copy the file
                shutil.copy2(source_path, destination_path)
    except FileNotFoundError as e:
        print(f"CSV file not found: {csv_file_path}")
        logging.error(f"CSV file not found: {csv_file_path}")
    except Exception as e:
        print(f"An error occurred: {e}")
        logging.error(f"An error occurred: {e}")

if __name__ == "__main__":
    # Path to the CSV file
    csv_file_path = r""
    
    # Path to the log file
    log_file_path = r""
    
    # Copy files with .htm extension and log missing documents
    copy_files_with_htm_extension(csv_file_path, log_file_path)
    
