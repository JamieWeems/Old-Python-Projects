import os

def search_string_in_file(file_path, search_string):
    """
    Searches for a specific string in a file.
    
    :param file_path: Path to the file.
    :param search_string: The string to search for.
    :return: True if the string is found, otherwise False.
    """
    try:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as file:
            for line in file:
                if search_string in line:
                    return True
        return False
    except Exception as e:
        print(f"Error reading file '{file_path}': {e}")
        return False

def search_string_in_directory(directory, search_string):
    """
    Searches for a specific string in all files within the specified directory (without searching subfolders).
    
    :param directory: Path to the directory.
    :param search_string: The string to search for.
    """
    try:
        for item in os.listdir(directory):
            item_path = os.path.join(directory, item)
            if os.path.isfile(item_path):
                if search_string_in_file(item_path, search_string):
                    print(f"String '{search_string}' found in file: {item_path}")
    except Exception as e:
        print(f"Error accessing directory '{directory}': {e}")

if __name__ == "__main__":
    # Specify the directory to search
    directory_to_search = r""
    
    # Specify the string to search for
    search_string = "your_search_string"
    
    # Search for the string in the directory
    search_string_in_directory(directory_to_search, search_string)

    # Pause to review the results
    input("Processing complete. Press Enter to exit...")