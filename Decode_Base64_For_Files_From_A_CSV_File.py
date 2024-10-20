import base64
import os
import csv

def decode_base64_file(file_path):
    try:
        # Open the file and read the base64 content
        with open(file_path, 'rb') as file:
            base64_content = file.read()

        # Decode the base64 content
        decoded_content = base64.b64decode(base64_content)

        # Write the decoded content back to the same file
        with open(file_path, 'wb') as file:
            file.write(decoded_content)
        
        print(f"Successfully decoded {file_path}")
        return True, ""
    except Exception as e:
        print(f"Error processing file {file_path}: {e}")
        return False, str(e)

def process_files_from_csv(input_csv_path, output_csv_path):
    results = []
    with open(input_csv_path, mode='r', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            file_path = row['source']

            print(f"Processing file: {file_path}")

            success, error_message = decode_base64_file(file_path)

            results.append({
                "source": file_path,
                "success": success,
                "error": error_message
            })

    with open(output_csv_path, mode='w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ["source", "success", "error"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(results)

    print(f"CSV report generated: {output_csv_path}")

if __name__ == "__main__":
    # Specify the input CSV file containing source paths, and the output CSV file path
    input_csv_path = r""
    output_csv_path = r""

    # Process the files and generate the CSV report
    process_files_from_csv(input_csv_path, output_csv_path)
