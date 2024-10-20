import os
import csv
from bs4 import BeautifulSoup
import logging

# Function to set up logging
def setup_logging(log_file_path):
    logging.basicConfig(
        filename=log_file_path,
        level=logging.ERROR,
        format='%(asctime)s:%(levelname)s:%(message)s'
    )

# Function to determine if the src is a URL and not base64
def is_url_not_base64(src):
    return src.startswith('http://') or src.startswith('https://') or src.endswith('.gif') or src.endswith('.GIF')  or src.endswith('.jpg') or src.endswith('.JPG')  or src.endswith('.jfif') or src.endswith('.JFIF') or src.endswith('.png') or src.endswith('.PNG') or src.endswith('.bmp') or src.endswith('.BMP') or src.endswith('.tif') or src.endswith('.TIF') or src.endswith('.tiff') or src.endswith('.TIFF') or src.endswith('.gif')

# Function to process HTML content and find img tags with src attributes that are URLs
def process_html_content(html_content, file_location, csv_writer):
    print(f"Processing content from file: {file_location}")
    soup = BeautifulSoup(html_content, 'html.parser')

    imgs = soup.find_all('img', src=True)

    for img in imgs:
        src = img['src']
        if is_url_not_base64(src):
            full_img_element = str(img)
            csv_writer.writerow([file_location, full_img_element, src])

# Function to read file with different encodings
def read_file_with_encoding(file_path, encoding):
    try:
        with open(file_path, 'r', encoding=encoding) as file:
            return file.read()
    except Exception as e:
        logging.error(f"Error reading file {file_path} with {encoding} encoding: {e}")
        print(f"Error reading file {file_path} with {encoding} encoding: {e}")
        return None

# Function to process HTML files in a directory
def process_html_files_in_directory(source_directory, csv_file_path):
    with open(csv_file_path, 'w', newline='', encoding='utf-8') as csv_file:
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow(['File Location', 'Full Img Element', 'Image URL'])

        for root, _, files in os.walk(source_directory):
            for file in files:
                if file.endswith('.html'):
                    file_location = os.path.join(root, file)
                    html_content = None
                    for encoding in ['utf-8', 'latin-1']:  # 'latin-1' is commonly used for ANSI
                        html_content = read_file_with_encoding(file_location, encoding)
                        if html_content:
                            print(f"Successfully read file: {file_location} with {encoding} encoding")
                            break
                    if html_content:
                        try:
                            process_html_content(html_content, file_location, csv_writer)
                        except Exception as e:
                            logging.error(f"Error processing file {file_location}: {e}")
                            print(f"Error processing file {file_location}: {e}")

if __name__ == "__main__":
    # Path to the directory containing HTML files
    source_directory = r""

    # Path to the output CSV file
    csv_file_path = r""

    # Path to the log file
    log_file_path = r""

    # Set up logging
    setup_logging(log_file_path)

    # Process HTML files and write to CSV
    process_html_files_in_directory(source_directory, csv_file_path)

    print("Processing complete. Check the CSV file for results.")
