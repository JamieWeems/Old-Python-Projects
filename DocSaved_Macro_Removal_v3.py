import os
import csv
import win32com.client as win32
import pythoncom
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed

# Define paths
csvFilePath = r""  # Path to the CSV file containing document paths
destinationDir = r""  # Destination folder for saving modified documents as PDF
logFilePath = r""  # Log file for errors
missingFilesLogPath = r""  # Log file for missing files

# Create destination folder if it doesn't exist
os.makedirs(destinationDir, exist_ok=True)

# Function to unlink fields in headers, footers, and main content, then save as PDF
def processWordDocument(docPath, destinationDir):
    pythoncom.CoInitialize()  # Initialize COM for this thread
    wordApp = win32.Dispatch('Word.Application')
    wordApp.Visible = False  # Set to False so Word remains hidden during the operation

    try:
        # Open the Word document
        doc = wordApp.Documents.Open(docPath)
        
        # Unlink fields in the main content
        doc.Content.Select()
        wordApp.Selection.WholeStory()
        wordApp.Selection.Fields.Unlink()

        # Unlink fields in headers and footers
        for section in doc.Sections:
            for header in section.Headers:
                if header.Exists:
                    header.Range.Fields.Unlink()
            for footer in section.Footers:
                if footer.Exists:
                    footer.Range.Fields.Unlink()

        # Construct new file name and save the modified document as PDF
        fileName = os.path.basename(docPath)
        newFileName = os.path.splitext(fileName)[0] + '_unlinked.pdf'
        destinationPdfPath = os.path.join(destinationDir, newFileName)

        # Save the document as PDF
        doc.ExportAsFixedFormat(destinationPdfPath, ExportFormat=17)  # 17 = PDF format
        doc.Close(False)  # Close the document without saving changes to the original

        print(f"Processed and saved: {destinationPdfPath}")

        return os.path.splitext(fileName)[0], True

    except Exception as e:
        errorMessage = f"Error processing {docPath}: {e}"
        print(errorMessage)
        logError(errorMessage)
        return os.path.splitext(fileName)[0], False

    finally:
        wordApp.Quit()
        pythoncom.CoUninitialize()  # Uninitialize COM for this thread

def logError(message):
    """Logs errors to the error log file."""
    with open(logFilePath, 'a') as logFile:
        logFile.write(f"{datetime.now()} - {message}\n")

def logMissingFile(fileName):
    """Logs missing files to the missing files log file."""
    with open(missingFilesLogPath, 'a') as logFile:
        logFile.write(f"{datetime.now()} - Missing file: {fileName}\n")

def processDocumentsConcurrently(csvFile, destinationDir, maxWorkers=5):
    """Processes Word documents concurrently listed in a CSV file."""
    processedFiles = []

    try:
        with open(csvFile, newline='') as file:
            reader = csv.reader(file)
            futures = []
            
            # Use ThreadPoolExecutor for concurrent processing
            with ThreadPoolExecutor(max_workers=maxWorkers) as executor:
                for row in reader:
                    docPath = row[0].strip()  # Assuming the CSV has a single column with document paths
                    if os.path.exists(docPath):
                        futures.append(executor.submit(processWordDocument, docPath, destinationDir))
                    else:
                        errorMessage = f"File not found: {docPath}"
                        print(errorMessage)
                        logError(errorMessage)

                # Collect results as they complete
                for future in as_completed(futures):
                    fileName, success = future.result()
                    if success:
                        processedFiles.append(fileName)

    except Exception as e:
        errorMessage = f"Error reading CSV file: {e}"
        print(errorMessage)
        logError(errorMessage)

    return processedFiles

def checkMissingFiles(csvFile, processedFiles):
    """Checks for documents that were not processed by comparing the destination folder with the CSV file."""
    try:
        # Get a list of expected document names (without extension) from the CSV
        expectedFiles = []
        with open(csvFile, newline='') as file:
            reader = csv.reader(file)
            for row in reader:
                fileName = os.path.basename(row[0].strip())
                expectedFiles.append(os.path.splitext(fileName)[0])

        # Compare expected files with the processed files list
        missingFiles = set(expectedFiles) - set(processedFiles)

        if missingFiles:
            for missing in missingFiles:
                errorMessage = f"File not processed: {missing}"
                print(errorMessage)
                logMissingFile(missing)  # Log the missing files to a separate log file
        else:
            print("All documents processed successfully.")

    except Exception as e:
        errorMessage = f"Error during file comparison: {e}"
        print(errorMessage)
        logError(errorMessage)

# Run the script with concurrency
processedFiles = processDocumentsConcurrently(csvFilePath, destinationDir, maxWorkers=5)

# Verify which documents were not processed and log them
checkMissingFiles(csvFilePath, processedFiles)

print(f"Process completed. Check error log for errors: {logFilePath}")
print(f"Missing files logged at: {missingFilesLogPath}")
