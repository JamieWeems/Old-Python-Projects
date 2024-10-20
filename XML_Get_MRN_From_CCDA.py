import os
import csv
import xml.etree.ElementTree as ET

def extract_attribute_from_xml(file_path, attribute_path):
    try:
        tree = ET.parse(file_path)
        root = tree.getroot()

        print(root)
        print(root[0].tag)
        print(root[10].tag)
        print(root[10][0].tag)
        print(root[10][0][0].tag)
        print(root[10][0][0].text)

        
        # Split the attribute_path to separate element path and attribute name
        element_path, attribute_name = attribute_path.rsplit('/@', 1)
        
        # Find the element at the specified path
        element = root.find(element_path)
        if element is not None:
            attribute_value = element.attrib.get(attribute_name)
            if attribute_value is not None:
                return attribute_value.strip()
        
        print(f"No attribute '{attribute_name}' found at path '{element_path}' in file {file_path}")
        return None
    except ET.ParseError as e:
        print(f"Error parsing XML file {file_path}: {e}")
        return None

def write_xml_to_csv(xml_directory, attribute_path, csv_file_path):
    data_points = []

    # Iterate through all XML files in the directory
    for filename in os.listdir(xml_directory):
        if filename.endswith('.xml'):
            file_path = os.path.join(xml_directory, filename)
            attribute_value = extract_attribute_from_xml(file_path, attribute_path)
            if attribute_value is not None:
                data_points.append([attribute_value, filename])

    # Write data points to CSV
    try:
        with open(csv_file_path, 'w', newline='') as csv_file:
            csv_writer = csv.writer(csv_file)
            # Write header
            csv_writer.writerow(['Attribute Value', 'Document Name'])
            # Write data
            csv_writer.writerows(data_points)
    except Exception as e:
        print(f"Error writing to CSV file {csv_file_path}: {e}")

if __name__ == "__main__":
    # Directory containing XML files
    xml_directory = r""
    
    # Path to the XML attribute (use XPath-like syntax)
    attribute_path = r'{urn:hl7-org:v3}ClinicalDocument/{urn:hl7-org:v3}recordTarget/{urn:hl7-org:v3}patientRole/{urn:hl7-org:v3}id[@extension]'  # Example: 'root/element/subelement/@attributeName'
    
    # Path to the output CSV file
    csv_file_path = r""
    
    # Process XML files and write to CSV
    write_xml_to_csv(xml_directory, attribute_path, csv_file_path)
