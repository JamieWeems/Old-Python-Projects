import xml.etree.ElementTree as ET
from PIL import Image, ImageDraw, ImageFont

def parse_leadtools_annotations(xml_file_path):
    tree = ET.parse(xml_file_path)
    root = tree.getroot()

    annotations = []
    for page_index, page in enumerate(root.findall('Page')):
        for obj in page.findall('.//Object'):
            obj_type = obj.tag
            points = []
            for point in obj.find('Points').findall('Point'):
                x = float(point.get('X'))
                y = float(point.get('Y'))
                points.append((x, y))

            text = None
            text_element = obj.find('.//TextOptions/Text')
            if text_element is not None:
                text = text_element.text

            annotation = {
                "type": obj_type,
                "points": points,
                "fore_color": obj.find('ForeColor').text if obj.find('ForeColor') is not None else "x0",
                "back_color": obj.find('BackColor').text if obj.find('BackColor') is not None else "xFFFFFF",
                "font": obj.find('Font').text if obj.find('Font') is not None else "Arial",
                "font_size": obj.find('Font').get('Size') if obj.find('Font') is not None else "12",
                "text": text,
                "page": page_index  # Using the index as the page number (0-based index)
            }
            annotations.append(annotation)
    
    return annotations

def annotate_tiff(tiff_path, annotations):
    try:
        # Open the multi-page TIFF file
        with Image.open(tiff_path) as img:
            # List to store modified images
            pages = []

            for i in range(img.n_frames):  # Iterate through all pages
                img.seek(i)  # Move to the ith frame
                draw = ImageDraw.Draw(img)

                for detail in annotations:
                    if detail["page"] == i:
                        rect = detail["points"]
                        
                        if detail["type"] == "AnnObjectNote":
                            font = ImageFont.truetype("arial.ttf", int(detail["font_size"]))
                            draw.text(rect[0], detail.get("text", ""), fill=detail["fore_color"], font=font)
                        elif detail["type"] == "AnnObjectContainer":
                            draw.rectangle(rect, outline=detail["fore_color"], width=5)
                
                # Append the modified image to the list of pages
                pages.append(img.copy())

            # Save all pages back to the TIFF file
            pages[0].save(tiff_path, save_all=True, append_images=pages[1:])
            print(f"Annotations applied to TIFF: {tiff_path}")
    except Exception as e:
        print(f"Error annotating TIFF {tiff_path}: {e}")

def apply_annotations(doc_path, xml_file_path, output_annotation_path):
    annotations = parse_leadtools_annotations(xml_file_path)
    
    if doc_path.lower().endswith(('.tif', '.tiff')):
        annotate_tiff(doc_path, annotations)
    else:
        print(f"Unsupported document type for {doc_path}")

if __name__ == "__main__":
    xml_file_path = r""
    doc_path = r""  # Should be .tif or .tiff
    
    apply_annotations(doc_path, xml_file_path, "")
