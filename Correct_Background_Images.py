import os
import csv
import base64
import logging
from bs4 import BeautifulSoup

# Set up logging
log_file_path = r"error_log_notes.log"  # Update this path as needed
logging.basicConfig(filename=log_file_path, level=logging.ERROR,
                    format='%(asctime)s - %(levelname)s - %(message)s')

# Define the static image path
static_image_path = r"CALENDAR.gif"  # Replace with your actual static image path

# Function to read a file with different encodings
def read_file_with_encodings(file_path):
    encodings = ['utf-8', 'latin-1']  # Add other encodings if needed
    for encoding in encodings:
        try:
            with open(file_path, 'r', encoding=encoding) as file:
                return file.read()
        except UnicodeDecodeError:
            continue
    raise ValueError(f"Could not decode file {file_path} with available encodings")

# Function to replace img src with base64 encoded image data
def replace_img_src_with_base64(html_content, static_image_path):
    with open(static_image_path, 'rb') as img_file:
        base64_data = base64.b64encode(img_file.read()).decode('utf-8')
    soup = BeautifulSoup(html_content, 'html.parser')
    for img in soup.find_all('img', src="images/CALENDAR.GIF"):
        img['src'] = f"data:image/gif;base64,{base64_data}"
    return str(soup)

# Function to replace non-breaking space characters
def replace_nbsp(html_content):
    return html_content.replace(u'\xa0', '&nbsp;')

# Function to encode an image as base64
def encode_image_base64(image_path):
    with open(image_path, 'rb') as img_file:
        return base64.b64encode(img_file.read()).decode('utf-8')

# Function to replace background image URLs with base64 encoded images
def replace_background_image_with_base64(html_content, image_url, image_base64):
    soup = BeautifulSoup(html_content, 'html.parser')
    for div in soup.find_all('div', style=True):
        style = div['style']
        if image_url in style:
            new_style = style.replace(image_url, f"data:image/jpeg;base64,{image_base64}")
            div['style'] = new_style
    return str(soup)

# Function to process each HTML file
def process_html_file(file_path, img_replacement_info):
    try:
        html_content = read_file_with_encodings(file_path)

        # Replace img src with base64 if needed
        html_content = replace_img_src_with_base64(html_content, static_image_path)

        # Replace background image URL with base64
        bg_replacement = img_replacement_info.get('bg_replacement')
        if bg_replacement:
            image_base64 = encode_image_base64(bg_replacement['image_path'])
            html_content = replace_background_image_with_base64(html_content, bg_replacement['image_url'], image_base64)

        # Replace non-breaking space characters
        html_content = replace_nbsp(html_content)

        # Write the updated HTML content back to the file
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(html_content)
    except Exception as e:
        logging.error(f"Error processing file {file_path}: {e}")
        print(f"Error processing file {file_path}: {e}")

# Main function to iterate through the CSV and process files
def main(csv_file_path):
    with open(csv_file_path, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            file_location = row['file_location']
            image_url = row['background_image_url']
            jpg_file_location = row['jpg_file_location']
            img_replacement_info = {
                'bg_replacement': {
                    'image_url': image_url,
                    'image_path': jpg_file_location
                }
            }
            process_html_file(file_location, img_replacement_info)

if __name__ == "__main__":
    csv_file_path = r"" # Replace with your CSV file path
    main(csv_file_path)
    print("Processing complete.")
