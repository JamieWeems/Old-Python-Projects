import os
import re
import shutil
import logging

def setup_logging(log_file_path):
    logging.basicConfig(
        filename=log_file_path,
        level=logging.WARNING,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )

def correct_textarea_tags(html_content):
    # Pattern to find self-closing textarea tags
    pattern = re.compile(r'<textarea([^>]*)/>')
    
    # Replace self-closing tags with opening and closing tags
    corrected_html = pattern.sub(r'<textarea\1></textarea>', html_content)
    
    return corrected_html

def correct_html_files_in_directory(source_directory, destination_directory, log_file_path):
    setup_logging(log_file_path)
    
    if not os.path.exists(destination_directory):
        os.makedirs(destination_directory)

    for root, dirs, files in os.walk(source_directory):
        for file_name in files:
            if file_name.endswith('.html'):
                source_file_path = os.path.join(root, file_name)
                relative_path = os.path.relpath(root, source_directory)
                destination_file_path = os.path.join(destination_directory, relative_path, file_name)

                # Create destination subdirectories if they don't exist
                destination_dir = os.path.dirname(destination_file_path)
                if not os.path.exists(destination_dir):
                    os.makedirs(destination_dir)

                try:
                    with open(source_file_path, 'r', encoding='utf-8') as file:
                        html_content = file.read()
                    
                    corrected_html = correct_textarea_tags(html_content)
                    
                    with open(destination_file_path, 'w', encoding='utf-8') as file:
                        file.write(corrected_html)
                    
                    print(f"Corrected HTML saved to {destination_file_path}")
                except FileNotFoundError:
                    print(f"File not found: {source_file_path}")
                    logging.warning(f"File not found: {source_file_path}")
                except Exception as e:
                    print(f"An error occurred with file {source_file_path}: {e}")
                    logging.error(f"An error occurred with file {source_file_path}: {e}")

if __name__ == "__main__":
    # Path to the source directory containing HTML files
    source_directory = r""
    
    # Path to the destination directory where corrected HTML files will be saved
    destination_directory = r""
    
    # Path to the log file
    log_file_path = r"log_file.log"
    
    # Correct HTML files in the source directory and save them to the destination directory
    correct_html_files_in_directory(source_directory, destination_directory, log_file_path)
