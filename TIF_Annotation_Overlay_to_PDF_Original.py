# pip commands to install required libraries:
# pip install Pillow
# 
# Note: base64, io, os, xml, and csv are part of Python's standard library,
# so they don't need to be installed separately.

import base64
import io
import os
import xml.etree.ElementTree as ET
from PIL import Image, ImageDraw, ImageFont
import csv

# List to store conversion details
conversion_log = []

def process_annotation_file(tiff_path, xml_path, output_pdf_path):
    print(f"Processing {tiff_path} with {xml_path}")
    
    try:
        tree = ET.parse(xml_path)
        root = tree.getroot()
    except ET.ParseError as e:
        print(f"Error parsing XML file {xml_path}: {e}")
        return
    
    pdf_pages = []
    with Image.open(tiff_path) as image:
        for page_num, page_element in enumerate(root.findall('Page'), start=1):
            if page_num > image.n_frames:
                print(f"Warning: XML has more pages than TIFF. Skipping extra XML pages.")
                break
            
            image.seek(page_num - 1)
            img_copy = image.copy().convert("RGBA")
            draw = ImageDraw.Draw(img_copy, 'RGBA')
            
            img_width, img_height = img_copy.size
            print(f"Page {page_num} dimensions: {img_width}x{img_height}")
            
            try:
                font = ImageFont.truetype("arial.ttf", 26)
            except IOError:
                print("Arial font not found. Using default font.")
                font = ImageFont.load_default()
            
            for obj in page_element.findall('.//Object'):
                if obj.text.strip() == 'AnnObjectNote':
                    process_note(obj, draw, font)
                elif obj.text.strip() == 'AnnObjectStamp':
                    process_stamp(obj, img_copy)
            
            pdf_pages.append(img_copy.convert("RGB"))
    
    if pdf_pages:
        pdf_pages[0].save(output_pdf_path, save_all=True, append_images=pdf_pages[1:])
        print(f"Processed and saved to {output_pdf_path}")
        # Log the conversion details
        conversion_log.append([os.path.dirname(tiff_path), os.path.basename(tiff_path), os.path.basename(output_pdf_path)])
    else:
        print(f"No pages processed for {tiff_path}")

def process_note(obj, draw, font):
    points = obj.find('.//Points')
    text_options = obj.find('.//TextOptions')
    
    if points is None or text_options is None:
        return
    
    coords = []
    for point in points.findall('Point'):
        x = float(point.get('X', 0))
        y = float(point.get('Y', 0))
        coords.append((int(x), int(y)))
    
    if len(coords) < 2:
        return
    
    left = min(coord[0] for coord in coords)
    top = min(coord[1] for coord in coords)
    right = max(coord[0] for coord in coords)
    bottom = max(coord[1] for coord in coords)
    
    text_content = text_options.find('Text').text if text_options.find('Text') is not None else ""
    
    bbox = font.getbbox(text_content)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    
    right = max(right, left + text_width + 20)
    bottom = max(bottom, top + text_height + 10)
    
    print(f"Drawing white filled rectangle: ({left}, {top}) to ({right}, {bottom}) for text: {text_content}")
    draw.rectangle([left, top, right, bottom], fill=(255, 255, 255, 200), outline=(0, 0, 0), width=2)  # White fill with slight transparency, black outline
    
    text_x = left + 10
    text_y = top + (bottom - top - text_height) // 2
    draw.text((text_x, text_y), text_content, font=font, fill=(0, 0, 0, 255))

def process_stamp(obj, img):
    bitmap = obj.find('.//Bitmap')
    if bitmap is None:
        return
    
    width = int(bitmap.get('Width', 0))
    height = int(bitmap.get('Height', 0))
    data = bitmap.find('Data').text
    
    if not data or width == 0 or height == 0:
        return
    
    # Decode base64 data
    image_data = base64.b64decode(data)
    
    # Create image from raw data
    stamp_image = Image.frombytes('RGBA', (width, height), image_data)
    
    # Flip the image vertically
    stamp_image = stamp_image.transpose(Image.FLIP_TOP_BOTTOM)
    
    # Get coordinates to paste the stamp
    points = obj.find('.//Points')
    if points is None or len(points.findall('Point')) < 2:
        return
    
    x = int(float(points.find('Point').get('X', 0)))
    y = int(float(points.find('Point').get('Y', 0)))
    
    # Paste the flipped stamp onto the main image
    img.paste(stamp_image, (x, y), stamp_image)
    print(f"Pasted stamp at ({x}, {y}) with dimensions {width}x{height}")

def find_annotation_file(tiff_path):
    base_name = os.path.splitext(os.path.basename(tiff_path))[0]
    possible_files = [
        f"{base_name}.xml",
        f"{base_name}_annotation.xml",
        f"{base_name}_annotations.xml"
    ]
    
    for annotation_file in possible_files:
        full_path = os.path.join(os.path.dirname(tiff_path), annotation_file)
        if os.path.exists(full_path):
            print(f"Found annotation file: {full_path}")
            return full_path
    
    print(f"No matching annotation file found for: {base_name}")
    return None

def process_tiff_directory(directory):
    for filename in os.listdir(directory):
        if filename.lower().endswith(('.tif', '.tiff')) and '_original' not in filename.lower():
            tiff_path = os.path.join(directory, filename)
            xml_path = find_annotation_file(tiff_path)
            
            if xml_path:
                output_pdf_path = os.path.splitext(tiff_path)[0] + ".pdf"
                process_annotation_file(tiff_path, xml_path, output_pdf_path)
            else:
                print(f"No matching annotation file for {tiff_path}")

def save_conversion_log(directory):
    log_path = os.path.join(directory, "conversion_log.csv")
    with open(log_path, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["Location", "Original Filename", "New Filename"])
        writer.writerows(conversion_log)
    print(f"Conversion log saved to {log_path}")

if __name__ == "__main__":
    # Directory containing the TIFF files and annotation XML files
    directory = r""
    
    # Process all TIFF files in the directory
    process_tiff_directory(directory)
    
    # Save the conversion log
    save_conversion_log(directory)

"""
How to use this script:

1. Ensure you have Python installed on your system.
2. Install the required library by running: pip install Pillow
3. Place this script in a convenient location.
4. Modify the 'directory' variable in the if __name__ == "__main__": block to point to the folder containing your TIFF and XML files.
5. Run the script from the command line: python script_name.py

The script will:
- Process all TIFF files in the specified directory
- Look for corresponding annotation XML files
- Apply text annotations with white backgrounds and black outlines
- Apply bitmap stamps (flipped vertically)
- Save the result as a PDF file with the same name as the original TIFF
- Create a CSV file named 'conversion_log.csv' in the same directory, listing all processed files

Note: Ensure that the TIFF files and their corresponding XML files are in the same directory.
The XML files should be named either <tiff_name>_annotation.xml or <tiff_name>_annotations.xml.
"""