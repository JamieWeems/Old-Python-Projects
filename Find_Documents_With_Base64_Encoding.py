import os
import base64
import csv

def is_base64_encoded(data):
    try:
        if isinstance(data, str):
            # Check if the string can be decoded from base64
            base64.b64decode(data)
        elif isinstance(data, bytes):
            # Check if the bytes can be decoded from base64
            base64.b64decode(data.decode('utf-8'))
        else:
            return False
        return True
    except Exception:
        return False

def check_files_in_directory(directory):
    base64_files = []

    for root, _, files in os.walk(directory):
        for file in files:
            if not file.lower().endswith('.rtf'):
                continue

            file_path = os.path.join(root, file)
            with open(file_path, 'rb') as f:
                content = f.read()
                # Check if the file starts with "{\rtf1\ansi"
                if content.startswith(b'{\\rtf1\\ansi'):
                    continue
                if is_base64_encoded(content):
                    base64_files.append(file_path)
    
    return base64_files

def write_to_csv(file_list, output_csv):
    with open(output_csv, 'w', newline='') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(['File Path'])
        for file in file_list:
            csvwriter.writerow([file])

# Specify the directory you want to scan and the output CSV file
directory_to_scan = r""
output_csv_file = r""

# Get the list of base64 encoded files
base64_files = check_files_in_directory(directory_to_scan)

# Write the list of base64 encoded files to a CSV file
write_to_csv(base64_files, output_csv_file)

print(f"Base64 encoded files have been written to {output_csv_file}")
