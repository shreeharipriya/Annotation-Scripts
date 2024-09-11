# Script to convert yolo annotations to voc format
import os
import xml.etree.cElementTree as ET
from PIL import Image
from math import floor

###########################
#set directories and class names
###########################
ANNOTATIONS_DIR_PREFIX = "/home/vvdn/OUTDOOR/s2cp"
IMAGE_DIR_PREFIX = "/home/vvdn/OUTDOOR/s2cp"
imgExt = "jpg"
imgChnls = 3 #RGB:3 ; Grayscale:1

DESTINATION_DIR = "/home/vvdn/OUTDOOR/s2cp"


CLASS_MAPPING = {
    '0': '0',
    '1': '1',
    '2': '2',
    '3': '3',
    '4': '4',
    '5': '5',
    '6': '6',
    '7': '7',
    '8': '8',
    '9': '9',
    '10': '10',
    '11': '11',
}

###########################

def create_root(file_prefix, width, height):
    root = ET.Element("annotations")
    ET.SubElement(root, "filename").text = "{}.{}".format(file_prefix,imgExt)
    ET.SubElement(root, "folder").text = "{}/{}.{}".format(IMAGE_DIR_PREFIX,file_prefix,imgExt)
    size = ET.SubElement(root, "size")
    ET.SubElement(size, "width").text = str(width)
    ET.SubElement(size, "height").text = str(height)
    ET.SubElement(size, "depth").text = str(imgChnls)
    return root


def create_object_annotation(root, voc_labels):
    for voc_label in voc_labels:
        obj = ET.SubElement(root, "object")
        ET.SubElement(obj, "name").text = voc_label[0]
        ET.SubElement(obj, "pose").text = "Unspecified"
        ET.SubElement(obj, "truncated").text = str(0)
        ET.SubElement(obj, "difficult").text = str(0)
        bbox = ET.SubElement(obj, "bndbox")
        ET.SubElement(bbox, "xmin").text = str(voc_label[1])
        ET.SubElement(bbox, "ymin").text = str(voc_label[2])
        ET.SubElement(bbox, "xmax").text = str(voc_label[3])
        ET.SubElement(bbox, "ymax").text = str(voc_label[4])
    return root


def create_file(file_prefix, width, height, voc_labels):
    root = create_root(file_prefix, width, height)
    root = create_object_annotation(root, voc_labels)
    tree = ET.ElementTree(root)
    

    tree.write("{}/{}.xml".format(DESTINATION_DIR, file_prefix))


def read_file(file_path):
    file_prefix = file_path.split(".txt")[0]
    image_file_name = "{}.{}".format(file_prefix,imgExt)
    img = Image.open("{}/{}".format(IMAGE_DIR_PREFIX, image_file_name))
    print(img)

    w, h = img.size
    prueba = "{}/{}".format(ANNOTATIONS_DIR_PREFIX, file_path)
    print(prueba)
    with open(prueba) as file:
        lines = file.readlines()
        voc_labels = []
        for line in lines:	
            voc = []
            line = line.strip()
            data = line.split()
            voc.append(CLASS_MAPPING.get(data[0]))
            bbox_width = float(data[3]) * w
            bbox_height = float(data[4]) * h
            center_x = float(data[1]) * w
            center_y = float(data[2]) * h
            voc.append(floor(center_x - (bbox_width / 2)))
            voc.append(floor(center_y - (bbox_height / 2)))
            voc.append(floor(center_x + (bbox_width / 2)))
            voc.append(floor(center_y + (bbox_height / 2)))
            voc_labels.append(voc)
        create_file(file_prefix, w, h, voc_labels)
    print("Processing complete for file: {}".format(file_path))


def start():
    if not os.path.exists(DESTINATION_DIR):
        os.makedirs(DESTINATION_DIR)
    for filename in os.listdir(ANNOTATIONS_DIR_PREFIX):
        if filename.endswith('txt'):
            try:
                PathFileName = "{}/{}".format(ANNOTATIONS_DIR_PREFIX, filename)
                if os.stat(PathFileName).st_size > 0:
                    print("Si")
                    read_file(filename) 
            except:
                print("No")         
            
        else:
            print("Skipping file: {}".format(filename))


if __name__ == "__main__":
    start()
