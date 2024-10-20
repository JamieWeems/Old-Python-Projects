import os
import base64
from bs4 import BeautifulSoup
import chardet
import logging

def setup_logging(log_file_path):
    logging.basicConfig(filename=log_file_path, level=logging.ERROR, 
                        format='%(asctime)s:%(levelname)s:%(message)s')

def detect_encoding(file_path):
    with open(file_path, 'rb') as file:
        raw_data = file.read()
    result = chardet.detect(raw_data)
    return result['encoding']

def convert_image_to_base64(image_path):
    with open(image_path, 'rb') as image_file:
        encoded_string = base64.b64encode(image_file.read()).decode('utf-8')
    return f"data:image/gif;base64,{encoded_string}"

def replace_nbsp(html_content):
    return html_content.replace(u'\xa0', '&nbsp;')

def process_html_file(file_path, image_data):
    encoding = detect_encoding(file_path)
    
    try:
        with open(file_path, 'r', encoding=encoding, errors='ignore') as file:
            soup = BeautifulSoup(file, 'html.parser')
        
        img_tags = soup.find_all('img', src="images/CALENDAR.GIF")
        
        for img in img_tags:
            img['src'] = image_data
        
        html_content = str(soup)
        html_content = replace_nbsp(html_content)
        
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(html_content)
        print(f"Processed {file_path}")
    except Exception as e:
        logging.error(f"Error processing {file_path}: {e}")

def process_html_files(directory, image_path, log_file_path):
    setup_logging(log_file_path)
    image_data = convert_image_to_base64(image_path)
    
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.lower().endswith('.html'):
                file_path = os.path.join(root, file)
                process_html_file(file_path, image_data)

if __name__ == "__main__":
    html_directory = r""
    image_path = r"\CALENDAR.gif"
    log_file_path = r"Calendar_GIF_Error.log"
    
    process_html_files(html_directory, image_path, log_file_path)

print("Processing complete. Check the CSV file for results.")