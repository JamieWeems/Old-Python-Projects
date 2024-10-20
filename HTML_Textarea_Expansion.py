import os
import logging
from math import ceil
from bs4 import BeautifulSoup

def setup_logging(log_file_path):
    logging.basicConfig(
        filename=log_file_path,
        level=logging.WARNING,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )

def calculate_height(content):
    base_height = 25  # base height in pixels
    char_height = 20  # approximate height of a character in pixels
    padding = 20  # additional padding

    content_lines = 0
    max_line_length = 0

    lines = content.split('\n')
    for line in lines:
        content_lines += 1
        max_line_length = max(max_line_length, len(line))

    # Calculate additional height based on line length
    additional_height = ceil(max_line_length / 250) * char_height
    height = base_height + content_lines * char_height + additional_height + padding

    return f"width: 100%; height: {height}px;"

def process_html_content(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')

    # Find all textarea tags
    textareas = soup.find_all('textarea')
    
    for textarea in textareas:
        if not textarea.string or not textarea.string.strip():
            # If textarea is empty or contains only whitespace, hide the textarea and its preceding span
            textarea['style'] = 'display:none;'
            prev_span = textarea.find_previous_sibling('span')
            if prev_span:
                prev_span['style'] = 'display:none;'
        else:
            # If textarea has content, update its style based on content length
            textarea['style'] = calculate_height(textarea.string)

    return str(soup)

def process_html_files_in_directory(source_directory, log_file_path):
    setup_logging(log_file_path)

    for root, dirs, files in os.walk(source_directory):
        for file_name in files:
            if file_name.endswith('.html'):
                source_file_path = os.path.join(root, file_name)

                try:
                    # Attempt to read the file with UTF-8 encoding
                    try:
                        with open(source_file_path, 'r', encoding='utf-8') as file:
                            html_content = file.read()
                    except UnicodeDecodeError:
                        # If UTF-8 decoding fails, fall back to ANSI encoding
                        with open(source_file_path, 'r', encoding='ansi') as file:
                            html_content = file.read()

                    updated_html = process_html_content(html_content)

                    with open(source_file_path, 'w', encoding='utf-8') as file:
                        file.write(updated_html)

                    print(f"Updated HTML saved to {source_file_path}")
                except FileNotFoundError:
                    print(f"File not found: {source_file_path}")
                    logging.warning(f"File not found: {source_file_path}")
                except Exception as e:
                    print(f"An error occurred with file {source_file_path}: {e}")
                    logging.error(f"An error occurred with file {source_file_path}: {e}")

if __name__ == "__main__":
    # Path to the source directory containing HTML files
    source_directory = r""

    # Path to the log file
    log_file_path = r"log_file.log"

    # Process HTML files in the source directory
    process_html_files_in_directory(source_directory, log_file_path)
