import os
import shutil

def process_documents_in_folder(folder_path):
    # Define the subfolder to save the renamed documents
    subfolder = os.path.join(folder_path, "rtf_files")
    
    # Create the subfolder if it does not exist
    if not os.path.exists(subfolder):
        os.makedirs(subfolder)
    
    # Open the file to write the first lines
    with open(os.path.join(folder_path, "first_lines.txt"), 'w') as output_file:
        # Open the file to write the list of all files in the folder
        with open(os.path.join(folder_path, "file_list.txt"), 'w') as file_list:
            # Iterate over all files in the folder
            for file_name in os.listdir(folder_path):
                file_path = os.path.join(folder_path, file_name)
                
                # Skip if it's not a file
                if not os.path.isfile(file_path):
                    continue
                
                # Write the file name to the file list
                file_list.write(f"{file_name}\n")
                
                # Read the first line of the document
                with open(file_path, 'r') as file:
                    first_line = file.readline().strip()
                
                # Write the first line to the output file
                output_file.write(f"{file_name}: {first_line}\n")
                
                # Check if "rtf" is in the first line
                if "rtf" in first_line:
                    # Create a new file name with .rtf extension
                    file_base, _ = os.path.splitext(file_name)
                    new_file_name = file_base + ".rtf"
                    new_file_path = os.path.join(subfolder, new_file_name)
                    
                    # Copy and rename the file
                    shutil.copy(file_path, new_file_path)
                    print(f"File copied and renamed to: {new_file_path}")

# Example usage
folder_path = ""
process_documents_in_folder(folder_path)

# Pause to review the results
input("Processing complete. Press Enter to exit...")
