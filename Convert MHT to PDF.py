import os
import email
import logging
import pdfkit

# Set up logging
logging.basicConfig(filename='mht_to_pdf_conversion.log', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

def convert_mht_to_pdf(mht_path, pdf_path):
    try:
        with open(mht_path, 'rb') as file:
            msg = email.message_from_bytes(file.read())
            html_content = None

            for part in msg.walk():
                content_type = part.get_content_type()
                
                if content_type == 'text/html':
                    html_content = part.get_payload(decode=True).decode('utf-8')
                    break

            if not html_content:
                raise ValueError("No HTML content found in the MHT document")

            # Save HTML content to a temporary file
            temp_html_path = pdf_path.replace('.pdf', '.html')
            with open(temp_html_path, 'w', encoding='utf-8') as html_file:
                html_file.write(html_content)

            # Convert HTML to PDF using pdfkit
            pdfkit.from_file(temp_html_path, pdf_path)

            # Remove the temporary HTML file
            os.remove(temp_html_path)

            logging.info(f"Successfully converted {mht_path} to {pdf_path}")

    except Exception as e:
        logging.error(f"Error converting {mht_path} to PDF: {e}")
        print(f"Error converting {mht_path} to PDF: {e}")

if __name__ == "__main__":
    source_directory = r""  # Replace with the path to your MHT files
    destination_directory = r"" # Replace with the path to save PDF files

    if not os.path.exists(destination_directory):
        os.makedirs(destination_directory)

    for filename in os.listdir(source_directory):
        if filename.lower().endswith('.mht'):
            mht_path = os.path.join(source_directory, filename)
            pdf_filename = f"{os.path.splitext(filename)[0]}.pdf"
            pdf_path = os.path.join(destination_directory, pdf_filename)
            convert_mht_to_pdf(mht_path, pdf_path)
