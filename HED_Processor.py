import csv
import subprocess
import os

def convert_hed_to_pdf_from_csv(highedit_converter_path, csv_file, destination_folder):
    # Open the CSV file and read file paths
    with open(csv_file, 'r') as file:
        reader = csv.reader(file)
        
        # Loop through each row (file path) in the CSV
        for row in reader:
            if row:
                source_file = row[0].strip()  # CSV row should contain the full path to the .hed file
                if os.path.exists(source_file) and source_file.endswith(".hed"):
                    # Define the destination file path
                    destination_file = os.path.join(destination_folder, os.path.basename(source_file).replace(".hed", ".pdf"))
                    
                    # Run the HighEdit Converter command
                    command = f'"{highedit_converter_path}" /s:"{source_file}" /d:"{destination_file}" /f:pdf'
                    try:
                        subprocess.run(command, shell=True, check=True)
                        print(f"Converted {source_file} to {destination_file}")
                    except subprocess.CalledProcessError as e:
                        print(f"Error converting {source_file}: {e}")
                else:
                    print(f"File {source_file} not found or not a valid .hed file.")

# Example usage
highedit_converter_path = r"C:\Program Files (x86)\Text Control GmbH\HighEdit Converter Plus\HighEditConvertCmd.exe"
csv_file = r"C:\Documents\list_of_files.csv"
destination_folder = r"C:\Documents\PDFs"

convert_hed_to_pdf_from_csv(highedit_converter_path, csv_file, destination_folder)
