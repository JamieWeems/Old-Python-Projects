import os
import logging

def setup_logging(log_file_path):
    logging.basicConfig(
        filename=log_file_path,
        level=logging.WARNING,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )

def replace_nbsp(html_content):
    # Replace non-breaking space characters with their HTML entity equivalent
    return html_content.replace(u'\xa0', '&nbsp;')

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

                    corrected_html = replace_nbsp(html_content)

                    with open(source_file_path, 'w', encoding='utf-8') as file:
                        file.write(corrected_html)

                    print(f"Corrected HTML saved to {source_file_path}")
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
