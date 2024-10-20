import os

def convert_utf16le_bom_to_utf8(source_file_path, destination_file_path):
    try:
        # Read the file with UTF-16 LE encoding
        with open(source_file_path, 'rb') as source_file:
            content = source_file.read()

        # Check for BOM and remove it
        bom = b'\xff\xfe'
        if content.startswith(bom):
            content = content[len(bom):]

        # Decode the content from UTF-16 LE
        decoded_content = content.decode('utf-16le')

        # Encode the content to UTF-8
        utf8_content = decoded_content.encode('utf-8')

        # Write the content to the destination file with UTF-8 encoding
        with open(destination_file_path, 'wb') as destination_file:
            destination_file.write(utf8_content)

        print(f"Successfully converted {source_file_path} to {destination_file_path} with UTF-8 encoding.")

    except FileNotFoundError:
        print(f"File not found: {source_file_path}")
    except UnicodeDecodeError as e:
        print(f"Failed to decode file {source_file_path}: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    # Path to the source file encoded in UTF-16 LE with BOM
    source_file_path = r""
    
    # Path to the destination file encoded in UTF-8
    destination_file_path = r""
    
    # Convert the source file to UTF-8 encoding
    convert_utf16le_bom_to_utf8(source_file_path, destination_file_path)
