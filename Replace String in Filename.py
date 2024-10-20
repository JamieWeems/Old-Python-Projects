import os
# Get the current working directory
directory = r""
# Get a list of all files in the current directory
files = os.listdir(directory)
# Iterate over each file in the directory
for file in files:
    # Check if the file name contains the string you want to replace
    if "New Text" in file:
        print(file)
        time.sleep(30) 
        # Replace the string with the new string using the string method replace()
        new_file = file.replace("New Text Document", "New Text Document DOC")
        print(new_file)
        time.sleep(30) 
        # Rename the file with the new name
        os.rename(file, new_file)