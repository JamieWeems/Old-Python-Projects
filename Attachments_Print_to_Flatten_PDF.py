import os
import win32print
import win32api

def print_to_pdf(input_pdf_path, output_pdf_path):
    # Get the default printer
    default_printer = win32print.GetDefaultPrinter()
    
    # Set the "Microsoft Print to PDF" printer as default
    printer_name = "Microsoft Print to PDF"
    win32print.SetDefaultPrinter(printer_name)

    # Print the PDF
    try:
        # Prepare the printing command
        print_command = f'print /d:"{printer_name}" "{input_pdf_path}"'
        
        # Set the output file name
        win32api.ShellExecute(
            0,
            "printto",
            input_pdf_path,
            f'"{printer_name}" "{output_pdf_path}"',
            ".",
            0
        )
        
        print(f"PDF saved successfully to {output_pdf_path}")
    
    finally:
        # Restore the default printer
        win32print.SetDefaultPrinter(default_printer)

# Path to the input PDF file
input_pdf_path = r""

# Path to the output PDF file
output_pdf_path = r""

print_to_pdf(input_pdf_path, output_pdf_path)
