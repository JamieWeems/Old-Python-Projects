import os
import shutil
import logging

# Setup logging
logging.basicConfig(filename='process_documents.log', level=logging.DEBUG, 
                    format='%(asctime)s %(levelname)s:%(message)s')

def process_documents_in_folder(folder_path):
    # Define the subfolder to save the renamed documents
    subfolder = os.path.join(folder_path, "rtf_files")
    
    # Create the subfolder if it does not exist
    if not os.path.exists(subfolder):
        os.makedirs(subfolder)
        logging.info(f"Created subfolder: {subfolder}")
    
    try:
        # Iterate over all files in the folder
        for file_name in os.listdir(folder_path):
            file_path = os.path.join(folder_path, file_name)
            
            # Skip if it's not a file
            if not os.path.isfile(file_path):
                continue
            
            try:
                # Read the first line of the document
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as file:
                    first_line = file.readline().strip()
                
                # Check if "rtf" is in the first line
                if "rtf" in first_line:
                    # Create a new file name with .rtf extension
                    file_base, _ = os.path.splitext(file_name)
                    new_file_name = file_base + ".rtf"
                    new_file_path = os.path.join(subfolder, new_file_name)
                    
                    # Copy and rename the file
                    shutil.copy(file_path, new_file_path)
                    logging.info(f"File copied and renamed to: {new_file_path}")
            except Exception as e:
                logging.error(f"Failed to process file {file_name}: {e}")
    except Exception as e:
        logging.critical(f"Failed to process folder {folder_path}: {e}")

# Example usage
folder_path = r""
process_documents_in_folder(folder_path)

# Pause to review the results
input("Processing complete. Press Enter to exit...")
