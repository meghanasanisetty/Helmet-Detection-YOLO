import cv2
import numpy as np
import os

# Paths
base_path = "data"
weights_path = os.path.join(base_path, "yolov3-helmet.weights")
config_path = os.path.join(base_path, "yolov3-helmet.cfg")
names_path = os.path.join(base_path, "helmet.names")
image_path = os.path.join(base_path, "helmet_detection.jpg")

# Load YOLO model
net = cv2.dnn.readNet(weights_path, config_path)

# Use OpenCV’s DNN backend (CPU mode)
net.setPreferableBackend(cv2.dnn.DNN_BACKEND_OPENCV)
net.setPreferableTarget(cv2.dnn.DNN_TARGET_CPU)

# Load class names
with open(names_path, "r") as f:
    classes = [line.strip() for line in f.readlines()]

# Load image
img = cv2.imread(image_path)
height, width, channels = img.shape

# Prepare the image for YOLO
blob = cv2.dnn.blobFromImage(img, 1/255.0, (416, 416), swapRB=True, crop=False)
net.setInput(blob)

# Get output layer names
layer_names = net.getLayerNames()
output_layers = [layer_names[i - 1] for i in net.getUnconnectedOutLayers()]

# Run forward pass
outs = net.forward(output_layers)

# Show info on screen
conf_threshold = 0.5
nms_threshold = 0.4
class_ids = []
confidences = []
boxes = []

for out in outs:
    for detection in out:
        scores = detection[5:]
        class_id = np.argmax(scores)
        confidence = scores[class_id]
        if confidence > conf_threshold:
            center_x = int(detection[0] * width)
            center_y = int(detection[1] * height)
            w = int(detection[2] * width)
            h = int(detection[3] * height)
            x = int(center_x - w / 2)
            y = int(center_y - h / 2)
            boxes.append([x, y, w, h])
            confidences.append(float(confidence))
            class_ids.append(class_id)

# Apply Non-Max Suppression
indexes = cv2.dnn.NMSBoxes(boxes, confidences, conf_threshold, nms_threshold)

# Draw boxes
font = cv2.FONT_HERSHEY_SIMPLEX
for i in range(len(boxes)):
    if i in indexes:
        x, y, w, h = boxes[i]
        label = str(classes[class_ids[i]])
        confidence = round(confidences[i], 2)
        color = (0, 255, 0) if "helmet" in label.lower() else (0, 0, 255)
        cv2.rectangle(img, (x, y), (x + w, y + h), color, 2)
        cv2.putText(img, f"{label} {confidence}", (x, y - 5), font, 0.6, color, 2)

# Show result
cv2.imshow("Helmet Detection", img)
cv2.waitKey(0)
cv2.destroyAllWindows()

