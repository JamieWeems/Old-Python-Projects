import os
import shutil

def copy_txt_files(source_directory, destination_directory):
    # Ensure destination directory exists
    if not os.path.exists(destination_directory):
        os.makedirs(destination_directory)
    
    # Iterate over all files in the source directory
    for root, dirs, files in os.walk(source_directory):
        for file in files:
            # Check if the file has a .txt extension
            if file.lower().endswith('.txt'):
                # Construct full file paths
                source_file_path = os.path.join(root, file)
                destination_file_path = os.path.join(destination_directory, file)
                
                try:
                    # Copy the file
                    shutil.copy2(source_file_path, destination_file_path)
                    print(f"Copied {source_file_path} to {destination_file_path}")
                except Exception as e:
                    print(f"Error copying {source_file_path} to {destination_file_path}: {e}")

if __name__ == "__main__":
    # Define source and destination directories
    source_directory = r""
    destination_directory = r""
    
    # Copy txt files from source to destination
    copy_txt_files(source_directory, destination_directory)
