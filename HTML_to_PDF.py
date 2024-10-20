import os
import logging
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

def setup_logging(log_file_path):
    logging.basicConfig(
        filename=log_file_path,
        level=logging.ERROR,
        format='%(asctime)s:%(levelname)s:%(message)s'
    )

def print_html_to_pdf(source_html_path, destination_pdf_path, driver_path):
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--print-to-pdf=' + destination_pdf_path)

    service = Service(driver_path)
    driver = webdriver.Chrome(service=service, options=options)
    
    try:
        driver.get('file://' + os.path.abspath(source_html_path))
        # Trigger the print (Chrome will automatically save as PDF to the path specified in options)
        driver.execute_script('window.print();')
        print(f"Successfully printed {source_html_path} to {destination_pdf_path}")
    except Exception as e:
        logging.error(f"Error printing {source_html_path} to PDF: {e}")
        print(f"Error printing {source_html_path} to PDF: {e}")
    finally:
        driver.quit()

if __name__ == "__main__":
    # Path to the directory containing HTML files
    source_directory = r""
    
    # Path to the directory where you want to save the PDF files
    destination_directory = r""
    
    # Path to the log file
    log_file_path = r"log_file.log"
    
    # Path to the Chrome WebDriver
    driver_path = r"C:\JweemsTestFolder\chromedriver.exe"

    # Set up logging
    setup_logging(log_file_path)

    # Ensure the destination directory exists
    if not os.path.exists(destination_directory):
        os.makedirs(destination_directory)

    # Iterate through HTML files in the source directory
    for filename in os.listdir(source_directory):
        if filename.endswith(".html"):
            source_html_path = os.path.join(source_directory, filename)
            destination_pdf_path = os.path.join(destination_directory, f"{os.path.splitext(filename)[0]}.pdf")
            print_html_to_pdf(source_html_path, destination_pdf_path, driver_path)

    print("All HTML files have been processed.")
