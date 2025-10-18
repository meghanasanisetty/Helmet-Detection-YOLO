import os
import xml.etree.ElementTree as ET

# Correct paths for your setup
annotations_dir = r"data/annotations"
output_dir = r"data/labels"
os.makedirs(output_dir, exist_ok=True)

# Define your class names
classes = ["helmet", "no_helmet", "bike"]

def convert(size, box):
    dw = 1. / size[0]
    dh = 1. / size[1]
    x = (box[0] + box[1]) / 2.0 - 1
    y = (box[2] + box[3]) / 2.0 - 1
    w = box[1] - box[0]
    h = box[3] - box[2]
    x = x * dw
    w = w * dw
    y = y * dh
    h = h * dh
    return (x, y, w, h)

for xml_file in os.listdir(annotations_dir):
    if not xml_file.endswith(".xml"):
        continue
    xml_path = os.path.join(annotations_dir, xml_file)
    tree = ET.parse(xml_path)
    root = tree.getroot()
    
    size = root.find("size")
    w = int(size.find("width").text)
    h = int(size.find("height").text)
    
    txt_name = xml_file.replace(".xml", ".txt")
    txt_path = os.path.join(output_dir, txt_name)
    
    with open(txt_path, "w") as out_file:
        for obj in root.iter("object"):
            cls = obj.find("name").text
            if cls not in classes:
                continue
            cls_id = classes.index(cls)
            xmlbox = obj.find("bndbox")
            b = (float(xmlbox.find("xmin").text), float(xmlbox.find("xmax").text),
                 float(xmlbox.find("ymin").text), float(xmlbox.find("ymax").text))
            bb = convert((w, h), b)
            out_file.write(f"{cls_id} {' '.join([str(a) for a in bb])}\n")

print("✅ Conversion complete! Labels saved in data/labels/")
