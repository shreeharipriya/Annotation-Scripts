import xml.etree.ElementTree as ET
import os

def convert_xml_to_yolo(xml_file, output_dir):
    # Parse XML file
    tree = ET.parse(xml_file)
    root = tree.getroot()

    # Extract image size
    size = root.find('size')
    width = int(size.find('width').text)
    height = int(size.find('height').text)

    # Prepare output file
    output_file = os.path.join(output_dir, os.path.splitext(os.path.basename(xml_file))[0] + '.txt')
    with open(output_file, 'w') as f:
        # Process each object in the XML
        for obj in root.findall('object'):
            class_name = obj.find('name').text
            bndbox = obj.find('bndbox')
            xmin = int(bndbox.find('xmin').text)
            ymin = int(bndbox.find('ymin').text)
            xmax = int(bndbox.find('xmax').text)
            ymax = int(bndbox.find('ymax').text)

            # Convert to YOLO format
            bbox_width = xmax - xmin
            bbox_height = ymax - ymin
            center_x = (xmin + xmax) / 2.0 / width
            center_y = (ymin + ymax) / 2.0 / height
            norm_width = bbox_width / width
            norm_height = bbox_height / height

            # Assuming class_id is the index of the class name in the class list
            class_id = 0  # Modify this as needed for your dataset

            # Write to output file
            f.write(f"{class_id} {center_x} {center_y} {norm_width} {norm_height}\n")

def convert_directory(input_dir, output_dir):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    for file in os.listdir(input_dir):
        if file.endswith('.xml'):
            convert_xml_to_yolo(os.path.join(input_dir, file), output_dir)

# Usage
input_directory = '/home/vvdn_23737/overhead_hard_model/labels'
output_directory = '/home/vvdn_23737/overhead_hard_model'
convert_directory(input_directory, output_directory)
