import os
import subprocess
import sys
import pkg_resources
import win32com.client
from email.parser import BytesParser
from email.policy import default
import re
import csv
import tempfile
import ctypes
from PIL import Image
import logging

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# List of required packages
REQUIRED_PACKAGES = ['pywin32', 'pillow']

# Function to install missing packages
def install_packages(packages):
    installed_packages = {pkg.key for pkg in pkg_resources.working_set}
    missing_packages = [pkg for pkg in packages if pkg not in installed_packages]
    if missing_packages:
        logging.info(f"Installing missing packages: {missing_packages}")
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', *missing_packages])

# Install missing packages
install_packages(REQUIRED_PACKAGES)

# Check for required software
def check_software_installed(software_paths):
    for software, path in software_paths.items():
        if not os.path.exists(path):
            logging.error(f"{software} is not installed or not found at {path}. Please install it before running the script.")
            sys.exit(1)

SOFTWARE_PATHS = {
    'wkhtmltopdf': r'C:\\Program Files\\wkhtmltopdf\\bin\\wkhtmltopdf.exe',
    'LibreOffice': r'C:\\Program Files\\LibreOffice\\program\\soffice.exe',
    'ImageMagick': r'C:\\Program Files\\ImageMagick-7.1.1-Q16-HDRI\\magick.exe',
}

check_software_installed(SOFTWARE_PATHS)

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

if not is_admin():
    logging.error("This script requires administrative privileges.")
    ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, __file__, None, 1)
    sys.exit()

def add_image_fit_css(html_file_path):
    try:
        with open(html_file_path, 'rb') as file:
            content = file.read()
        content = content.replace(b'<head>', b'<head><style>img {max-width: 100%; height: auto;}</style>')
        with open(html_file_path, 'wb') as file:
            file.write(content)
    except Exception as e:
        logging.error(f"Error adding CSS to {html_file_path}: {e}")

def convert_msg_to_pdf(msg_file_path, pdf_file_path):
    outlook = win32com.client.Dispatch('Outlook.Application')
    mail = outlook.CreateItemFromTemplate(msg_file_path)
    try:
        with tempfile.TemporaryDirectory() as attachment_dir:
            cid_map = {}
            for attachment in mail.Attachments:
                try:
                    attachment_path = os.path.join(attachment_dir, attachment.FileName)
                    attachment.SaveAsFile(attachment_path)
                    cid = attachment.PropertyAccessor.GetProperty("http://schemas.microsoft.com/mapi/proptag/0x3712001F") or attachment.FileName
                    cid = re.sub(r'[<>]', '', cid)
                    cid_map[cid] = 'file:///' + attachment_path.replace("\\", "/")
                except Exception as e:
                    logging.error(f"Error saving attachment {attachment.FileName}: {e}")
                    continue

            html_body = mail.HTMLBody
            for cid, file_url in cid_map.items():
                html_body = re.sub(f'cid:{re.escape(cid)}', file_url, html_body, flags=re.IGNORECASE)
            combined_html = f"{html_body}"
            mhtml_file_path = pdf_file_path.replace('.pdf', '.html')
            with open(mhtml_file_path, 'w', encoding='utf-8') as f:
                f.write(combined_html)

            if os.path.exists(mhtml_file_path):
                add_image_fit_css(mhtml_file_path)
                result = subprocess.run([
                    SOFTWARE_PATHS['wkhtmltopdf'],
                    '--disable-local-file-access',
                    '--allow', os.path.dirname(mhtml_file_path),
                    '--image-quality', '15',
                    '--page-size', 'A4',
                    '--enable-local-file-access',
                    '--zoom', '0.75',
                    '--margin-top', '10mm',
                    '--margin-bottom', '10mm',
                    '--margin-left', '10mm',
                    '--margin-right', '10mm',
                    mhtml_file_path,
                    pdf_file_path
                ], check=True)
                if result.returncode == 0:
                    logging.info(f"Successfully converted {msg_file_path} to {pdf_file_path}")
                else:
                    logging.error(f"Error converting {msg_file_path} to {pdf_file_path}: {result.stderr}")
                return result.returncode == 0
            else:
                logging.error(f"Error: HTML file was not created: {mhtml_file_path}")
                return False
    except Exception as e:
        logging.error(f"Error converting {msg_file_path} to {pdf_file_path}: {e}")
        return False
    finally:
        mail.Close(0)

def convert_eml_to_pdf(eml_file_path, pdf_file_path):
    try:
        with open(eml_file_path, 'rb') as f:
            msg = BytesParser(policy=default).parse(f)

        mhtml_file_path = pdf_file_path.replace('.pdf', '.html')
        attachments_html = ''

        with tempfile.TemporaryDirectory() as attachment_dir:
            cid_map = {}

            for part in msg.iter_attachments():
                filename = part.get_filename()
                if filename:
                    filepath = os.path.join(attachment_dir, filename)
                    with open(filepath, 'wb') as att_file:
                        att_file.write(part.get_payload(decode=True))
                    cid = part.get('Content-ID')
                    if cid:
                        cid = cid.strip('<>')
                        cid_map[cid] = 'file:///' + filepath.replace("\\", "/")
                    if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.gif')):
                        attachments_html += f'<p>Attachment: <img src="data:image/jpeg;base64,{base64.b64encode(open(filepath, "rb").read()).decode()}" alt="{filename}" /></p>'
                    else:
                        attachments_html += f'<p>Attachment: <a href="{filepath}">{filename}</a></p>'

            body = msg.get_body(preferencelist=('html', 'plain')).get_content()

            for cid, file_url in cid_map.items():
                body = re.sub(f'cid:{re.escape(cid)}', file_url, body)

            mail_html = f'{body}{attachments_html}'

            with open(mhtml_file_path, 'w', encoding='utf-8') as f:
                f.write(mail_html)

            if os.path.exists(mhtml_file_path):
                add_image_fit_css(mhtml_file_path)
                result = subprocess.run([
                    SOFTWARE_PATHS['wkhtmltopdf'],
                    '--disable-local-file-access',
                    '--allow', os.path.dirname(mhtml_file_path),
                    '--image-quality', '15',
                    '--page-size', 'A4',
                    '--enable-local-file-access',
                    '--zoom', '0.75',
                    '--margin-top', '10mm',
                    '--margin-bottom', '10mm',
                    '--margin-left', '10mm',
                    '--margin-right', '10mm',
                    mhtml_file_path,
                    pdf_file_path
                ], check=True)
                if result.returncode == 0:
                    logging.info(f"Successfully converted {eml_file_path} to {pdf_file_path}")
                else:
                    logging.error(f"Error converting {eml_file_path} to {pdf_file_path}: {result.stderr}")
                return result.returncode == 0
            else:
                logging.error(f"Error: MHTML file was not created: {mhtml_file_path}")
                return False
    except Exception as e:
        logging.error(f"Error converting {eml_file_path} to {pdf_file_path}: {e}")
        return False

def convert_dat_to_pdf(dat_file_path, pdf_file_path):
    try:
        html_file_path = pdf_file_path.replace('.pdf', '.html')
        with open(dat_file_path, 'r') as file:
            lines = file.readlines()
        with open(html_file_path, 'w') as file:
            file.write('<html><body><pre>\n')
            file.writelines(lines)
            file.write('</pre></body></html>')
        if os.path.exists(html_file_path):
            result = subprocess.run([
                SOFTWARE_PATHS['wkhtmltopdf'],
                html_file_path,
                pdf_file_path
            ], check=True)
            if result.returncode == 0:
                logging.info(f"Successfully converted {dat_file_path} to {pdf_file_path}")
            else:
                logging.error(f"Error converting {dat_file_path} to {pdf_file_path}: {result.stderr}")
            return result.returncode == 0
        else:
            logging.error(f"Error: HTML file was not created: {html_file_path}")
            return False
    except Exception as e:
        logging.error(f"Error converting {dat_file_path} to {pdf_file_path}: {e}")
        return False

def convert_doc_to_pdf(doc_file_path, pdf_file_path):
    try:
        word = win32com.client.Dispatch('Word.Application')
        doc = word.Documents.Open(doc_file_path)
        doc.SaveAs(pdf_file_path, FileFormat=17)
        doc.Close()
        word.Quit()
        logging.info(f"Successfully converted {doc_file_path} to {pdf_file_path}")
        return True
    except Exception as e:
        logging.error(f"Error converting {doc_file_path} to {pdf_file_path}: {e}")
        return False

def convert_html_to_pdf(html_file_path, pdf_file_path):
    try:
        result = subprocess.run([
            SOFTWARE_PATHS['wkhtmltopdf'],
            '--disable-local-file-access',
            '--allow', os.path.dirname(html_file_path),
            '--image-quality', '15',
            '--page-size', 'A4',
            '--enable-local-file-access',
            '--zoom', '0.75',
            '--margin-top', '10mm',
            '--margin-bottom', '10mm',
            '--margin-left', '10mm',
            '--margin-right', '10mm',
            html_file_path,
            pdf_file_path
        ], check=True)
        if result.returncode == 0:
            logging.info(f"Successfully converted {html_file_path} to {pdf_file_path}")
        else:
            logging.error(f"Error converting {html_file_path} to {pdf_file_path}: {result.stderr}")
        return result.returncode == 0
    except Exception as e:
        logging.error(f"Error converting {html_file_path} to {pdf_file_path}: {e}")
        return False

def convert_odt_to_pdf(odt_file_path, pdf_file_path):
    try:
        result = subprocess.run([
            SOFTWARE_PATHS['LibreOffice'],
            '--headless',
            '--convert-to', 'pdf',
            '--outdir', os.path.dirname(pdf_file_path),
            odt_file_path
        ], check=True)
        if result.returncode == 0:
            logging.info(f"Successfully converted {odt_file_path} to {pdf_file_path}")
        else:
            logging.error(f"Error converting {odt_file_path} to {pdf_file_path}: {result.stderr}")
        return result.returncode == 0
    except Exception as e:
        logging.error(f"Error converting {odt_file_path} to {pdf_file_path}: {e}")
        return False

def convert_heic_to_pdf(heic_file_path, pdf_file_path):
    try:
        result = subprocess.run([
            SOFTWARE_PATHS['ImageMagick'], heic_file_path, pdf_file_path
        ], check=True)
        if result.returncode == 0:
            logging.info(f"Successfully converted {heic_file_path} to {pdf_file_path}")
        else:
            logging.error(f"Error converting {heic_file_path} to {pdf_file_path}: {result.stderr}")
        return result.returncode == 0
    except Exception as e:
        logging.error(f"Error converting {heic_file_path} to {pdf_file_path}: {e}")
        return False

def convert_jfif_to_pdf(jfif_file_path, pdf_file_path):
    try:
        result = subprocess.run([
            SOFTWARE_PATHS['ImageMagick'], jfif_file_path, pdf_file_path
        ], check=True)
        if result.returncode == 0:
            logging.info(f"Successfully converted {jfif_file_path} to {pdf_file_path}")
        else:
            logging.error(f"Error converting {jfif_file_path} to {pdf_file_path}: {result.stderr}")
        return result.returncode == 0
    except Exception as e:
        logging.error(f"Error converting {jfif_file_path} to {pdf_file_path}: {e}")
        return False

def convert_gif_to_pdf(gif_file_path, pdf_file_path):
    try:
        result = subprocess.run([
            SOFTWARE_PATHS['ImageMagick'], gif_file_path, pdf_file_path
        ], check=True)
        if result.returncode == 0:
            logging.info(f"Successfully converted {gif_file_path} to {pdf_file_path}")
        else:
            logging.error(f"Error converting {gif_file_path} to {pdf_file_path}: {result.stderr}")
        return result.returncode == 0
    except Exception as e:
        logging.error(f"Error converting {gif_file_path} to {pdf_file_path}: {e}")
        return False

def convert_oxps_to_pdf(oxps_file_path, pdf_file_path):
    try:
        result = subprocess.run([
            SOFTWARE_PATHS['LibreOffice'],
            '--headless',
            '--convert-to', 'pdf',
            '--outdir', os.path.dirname(pdf_file_path),
            oxps_file_path
        ], check=True)
        if result.returncode == 0:
            logging.info(f"Successfully converted {oxps_file_path} to {pdf_file_path}")
        else:
            logging.error(f"Error converting {oxps_file_path} to {pdf_file_path}: {result.stderr}")
        return result.returncode == 0
    except Exception as e:
        logging.error(f"Error converting {oxps_file_path} to {pdf_file_path}: {e}")
        return False

def convert_image_to_pdf(image_file_path, pdf_file_path):
    try:
        with Image.open(image_file_path) as img:
            img.convert('RGB').save(pdf_file_path, 'PDF')
        logging.info(f"Successfully converted {image_file_path} to {pdf_file_path}")
        return True
    except Exception as e:
        logging.error(f"Error converting {image_file_path} to {pdf_file_path}: {e}")
        return False

def convert_d01_to_pdf(d01_file_path, pdf_file_path):
    try:
        with open(d01_file_path, 'rb') as file:
            header = file.read(2)
        
        if header == b'BM':
            logging.info(f"{d01_file_path} is identified as a BMP file.")
            return convert_image_to_pdf(d01_file_path, pdf_file_path)
        elif header == b'\xff\xd8':
            logging.info(f"{d01_file_path} is identified as a JPG file.")
            return convert_image_to_pdf(d01_file_path, pdf_file_path)
        else:
            logging.warning(f"Unrecognized file format for {d01_file_path}.")
            return False
    except Exception as e:
        logging.error(f"Error converting {d01_file_path} to {pdf_file_path}: {e}")
        return False

def process_files_from_folder(folder_path):
    pdf_subfolder = os.path.join(folder_path, 'Converted_PDFs')
    if not os.path.exists(pdf_subfolder):
        os.makedirs(pdf_subfolder)

    converted_files = []

    conversion_functions = {
        '.msg': convert_msg_to_pdf,
        '.eml': convert_eml_to_pdf,
        '.txt': convert_doc_to_pdf,
        '.doc': convert_doc_to_pdf,
        '.docx': convert_doc_to_pdf,
        '.html': convert_html_to_pdf,
        '.mht': convert_html_to_pdf,
        '.odt': convert_odt_to_pdf,
        '.heic': convert_heic_to_pdf,
        '.oxps': convert_oxps_to_pdf,
        '.jfif': convert_jfif_to_pdf,
        '.gif': convert_gif_to_pdf,
        '.jp2': convert_image_to_pdf,
        '.pcx': convert_image_to_pdf,
        '.d01': convert_d01_to_pdf  # Handle .d01 files
    }

    for root, _, files in os.walk(folder_path):
        for file in files:
            file_path = os.path.join(root, file)
            file_extension = os.path.splitext(file)[1].lower()
            pdf_file_name = os.path.splitext(file)[0] + '.pdf'
            pdf_file_path = os.path.join(pdf_subfolder, pdf_file_name)

            if not os.path.exists(file_path):
                logging.warning(f"File does not exist: {file_path}")
                continue

            logging.info(f"Processing {file_path}...")

            success = False
            if file_extension in conversion_functions:
                success = conversion_functions[file_extension](file_path, pdf_file_path)
            elif file_extension == '.dat':
                if file_path.lower().endswith('.doc.dat'):
                    success = convert_doc_to_pdf(file_path, pdf_file_path)
                elif file_path.lower().endswith('.docx.dat'):
                    success = convert_doc_to_pdf(file_path, pdf_file_path)
                elif file_path.lower().endswith('.html.dat'):
                    success = convert_html_to_pdf(file_path, pdf_file_path)
                elif file_path.lower().endswith('.odt.dat'):
                    success = convert_odt_to_pdf(file_path, pdf_file_path)
                else:
                    success = convert_dat_to_pdf(file_path, pdf_file_path)
            else:
                logging.warning(f"Unsupported file extension: {file_extension}")
                continue

            converted_files.append({
                'NewPath': pdf_file_path if success else file_path,
                'OriginalPath': file_path,
                'Status': 'Success' if success else 'Failed'
            })

    output_csv_path = os.path.join(folder_path, 'conversion_results.csv')
    with open(output_csv_path, 'w', newline='') as csvfile:
        fieldnames = ['NewPath', 'OriginalPath', 'Status']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for item in converted_files:
            writer.writerow(item)

# Example usage
folder_path = r""
process_files_from_folder(folder_path)
