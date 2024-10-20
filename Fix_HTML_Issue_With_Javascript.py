import os
import logging
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

def setup_logging(log_file_path):
    logging.basicConfig(
        filename=log_file_path,
        level=logging.WARNING,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )

def process_html_content(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')

    # Find all textarea tags
    textareas = soup.find_all('textarea')

    for textarea in textareas:
        if not textarea.string or not textarea.string.strip():
            # If textarea is empty or contains only whitespace, hide the textarea and its preceding span
            textarea['style'] = 'display:none;'
            prev_span = textarea.find_previous_sibling('span')
            if (prev_span and prev_span.name == 'span'):
                prev_span['style'] = 'display:none;'

    return str(soup)

def process_html_file_with_selenium(file_path):
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')

    driver = webdriver.Chrome(options=chrome_options)

    try:
        driver.get(f'file://{os.path.abspath(file_path)}')

        # Run the provided JavaScript
        js_script = """
        var textareas = document.querySelectorAll('textarea')
            for (var i = 0; i < textareas.length; i++) {
                var textarea = textareas[i];
                var div = document.createElement('div');
                if (textarea.value != '') {
                    div.style = 'border: 1px solid black; white-space; pre-wrap;';
                    div.textContent = textarea.value;
                    div.className = 'converted-div';
                    textarea.parentNode.replaceChild(div, textarea);
                }
            }
        var inputs = document.querySelectorAll('input#complaint, [id$=Other]')
            for (var j = 0; j < inputs.length; j++) {
                var input = inputs[j];
                var divInput = document.createElement('div');
                divInput.style = 'border: 1px solid black; min-height: 22px';
                divInput.textContent = input.value;
                divInput.className = 'converted-div';
                input.parentNode.replaceChild(divInput, input);
            }
        """
        driver.execute_script(js_script)

        # Save the modified HTML back to the file
        modified_html = driver.page_source
        modified_html = process_html_content(modified_html)

        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(modified_html)

    except Exception as e:
        print(f"An error occurred with file {file_path}: {e}")
        logging.error(f"An error occurred with file {file_path}: {e}")

    finally:
        driver.quit()

def process_html_files_in_directory(source_directory, log_file_path):
    setup_logging(log_file_path)

    for root, dirs, files in os.walk(source_directory):
        for file_name in files:
            if file_name.endswith('.html'):
                source_file_path = os.path.join(root, file_name)

                try:
                    process_html_file_with_selenium(source_file_path)
                    print(f"Processed HTML file: {source_file_path}")
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
