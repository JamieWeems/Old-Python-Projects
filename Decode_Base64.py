import base64
import os

def decode_base64_file(source_file_path, destination_file_path):
    try:
        # Open the source file and read the base64 content
        with open(source_file_path, 'rb') as file:
            base64_content = file.read()

        # Decode the base64 content
        decoded_content = base64.b64decode(base64_content)

        # Write the decoded content to the destination file
        with open(destination_file_path, 'wb') as file:
            file.write(decoded_content)
        
        print(f"Successfully decoded {source_file_path} and saved to {destination_file_path}")
    
    except Exception as e:
        print(f"Error processing file {source_file_path}: {e}")

if __name__ == "__main__":
    # Path to the source file containing base64 content
    source_file_path = r""

    # Path to the destination file to save the decoded content
    destination_file_path = r""

    # Decode the base64 content and save to the destination file
    decode_base64_file(source_file_path, destination_file_path)
