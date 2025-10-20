import os
import xml.etree.ElementTree as ET

# --- CONFIG ---
annotations_dir = r"data/annotations"
images_dir = r"data/images"
output_labels_dir = r"data/labels"

# Create output folder if not exists
os.makedirs(output_labels_dir, exist_ok=True)

# Define your classes here
classes = ["With Helmet", "Without Helmet"]  # change if your dataset has different class names

def convert_bbox(size, box):
    """Convert Pascal VOC bbox to YOLO format"""
    dw = 1.0 / size[0]
    dh = 1.0 / size[1]
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

    image_name = root.find("filename").text
    image_name_no_ext = os.path.splitext(image_name)[0]
    size = root.find("size")
    w = int(size.find("width").text)
    h = int(size.find("height").text)

    label_file = os.path.join(output_labels_dir, image_name_no_ext + ".txt")

    with open(label_file, "w") as out_file:
        for obj in root.iter("object"):
            cls = obj.find("name").text
            if cls not in classes:
                print(f"⚠️ Skipping unknown class: {cls}")
                continue
            cls_id = classes.index(cls)
            xmlbox = obj.find("bndbox")
            b = (
                float(xmlbox.find("xmin").text),
                float(xmlbox.find("xmax").text),
                float(xmlbox.find("ymin").text),
                float(xmlbox.find("ymax").text),
            )
            bb = convert_bbox((w, h), b)
            out_file.write(f"{cls_id} {' '.join([str(a) for a in bb])}\n")

print("✅ Conversion complete! Labels saved in:", output_labels_dir)