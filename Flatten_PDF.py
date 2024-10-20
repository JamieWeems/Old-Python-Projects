import fitz  # PyMuPDF
import csv
import os

def flatten_pdf(input_pdf_path, output_pdf_path):
    try:
        doc = fitz.open(input_pdf_path)
        new_doc = fitz.open()

        for page_num in range(len(doc)):
            page = doc.load_page(page_num)
            pix = page.get_pixmap()
            new_page = new_doc.new_page(width=page.rect.width, height=page.rect.height)
            new_page.insert_image(new_page.rect, pixmap=pix)

        # Ensure the destination directory exists
        os.makedirs(os.path.dirname(output_pdf_path), exist_ok=True)
        
        new_doc.save(output_pdf_path)  # This will overwrite the file if it exists
        new_doc.close()
        doc.close()
        return True, ""
    except Exception as e:
        return False, str(e)

def process_pdfs_from_csv(input_csv_path, output_csv_path):
    results = []
    with open(input_csv_path, mode='r', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            input_pdf_path = row['source']
            output_pdf_path = row['destination']

            print(f"Processing file: {input_pdf_path}")

            success, error_message = flatten_pdf(input_pdf_path, output_pdf_path)

            if success:
                print(f"Successfully processed: {input_pdf_path}")
            else:
                print(f"Failed to process: {input_pdf_path} - Error: {error_message}")

            results.append({
                "source": input_pdf_path,
                "destination": output_pdf_path,
                "success": success,
                "error": error_message
            })

    with open(output_csv_path, mode='w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ["source", "destination", "success", "error"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(results)

    print(f"CSV report generated: {output_csv_path}")

# Specify the input CSV file containing source and destination paths, and the output CSV file path
input_csv_path = r""
output_csv_path = r""

# Process the PDFs and generate the CSV report
process_pdfs_from_csv(input_csv_path, output_csv_path)
