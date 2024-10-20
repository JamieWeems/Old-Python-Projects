from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import time
import os

# Path to your ChromeDriver
chrome_driver_path = r"C:\JweemsTestFolder\chromedriver.exe"

# Path to the MHT file
mht_file_path = r""

# Set up Chrome options
chrome_options = Options()
chrome_options.add_argument('--headless')  # Run Chrome in headless mode
chrome_options.add_argument('--disable-gpu')
chrome_options.add_argument('--print-to-pdf')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')

# Create a new Chrome session
service = Service(chrome_driver_path)
driver = webdriver.Chrome(service=service, options=chrome_options)

try:
    # Open the MHT file in Chrome
    driver.get(mht_file_path)
    time.sleep(5)  # Wait for the file to load

    # Trigger print (Ctrl + P) to save as PDF
    driver.execute_script('window.print();')
    time.sleep(5)  # Wait for the print dialog to complete

finally:
    # Close the browser
    driver.quit()

print("PDF saved successfully")
