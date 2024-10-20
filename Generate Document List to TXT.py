import os
 
def write_document_names_to_txt(folder_path, output_file_path):
    # Open the output file in write mode
    with open(output_file_path, 'w') as output_file:
        # Iterate over all files in the specified folder
        for file_name in os.listdir(folder_path):
            file_path = os.path.join(folder_path, file_name)
            # Skip if it's not a file
            if not os.path.isfile(file_path):
                continue
            # Write the file name to the output file
            output_file.write(f"{file_name}\n")
    print(f"Document names have been written to {output_file_path}")
 
# Example usage
folder_path = r""
output_file_path = r""
write_document_names_to_txt(folder_path, output_file_path)

# Pause to review the results
input("Processing complete. Press Enter to exit...")