import os
import csv
from datetime import datetime

def get_files_in_directory(directory):
    """
    Retrieves the file paths and last modified dates for all files in the specified directory.
    
    :param directory: Path to the directory.
    :return: List of tuples containing file paths and their last modified dates.
    """
    files_data = []
    
    for root, dirs, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)
            last_modified_date = datetime.fromtimestamp(os.path.getmtime(file_path)).strftime('%Y-%m-%d %H:%M:%S')
            files_data.append((file_path, last_modified_date))
    
    return files_data

def write_to_csv(files_data, csv_file_path):
    """
    Writes the file paths and last modified dates to a CSV file.
    
    :param files_data: List of tuples containing file paths and their last modified dates.
    :param csv_file_path: Path to the output CSV file.
    """
    with open(csv_file_path, mode='w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['file_path', 'last_modified_date'])
        
        for file_path, last_modified_date in files_data:
            writer.writerow([file_path, last_modified_date])

if __name__ == "__main__":
    # Specify the directory to scan
    directory_to_scan = r"H:\DacClientData\H900s\H976\Legacy Data\Final Documents\OAM North PT\aafdedfc6a742136f0683e745d3e8d296c5b691497de13ac0f28d92e77f3c99b\patient-doc"
    
    # Specify the path to the output CSV file
    output_csv_file_path = r"H:\DacClientData\H900s\H976\Legacy Data\Final Documents\OAM North PT\aafdedfc6a742136f0683e745d3e8d296c5b691497de13ac0f28d92e77f3c99b\H976_Document_Metadata_OAM North PT.csv"
    
    # Get the file data
    files_data = get_files_in_directory(directory_to_scan)
    
    # Write the file data to the CSV file
    write_to_csv(files_data, output_csv_file_path)

    print(f"File paths and last modified dates have been written to '{output_csv_file_path}'.")
    
    # Pause to review the results
    input("Processing complete. Press Enter to exit...")
