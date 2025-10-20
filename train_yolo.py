from ultralytics import YOLO

# Load YOLOv8n model (lightweight)
model = YOLO("yolov8n.pt")

# Train on your dataset
results = model.train(
    data="data.yaml",       # path to your YAML file
    epochs=50,              # you can adjust later (start small)
    imgsz=640,              # image size
    batch=8,                # batch size
    name="helmet_yolov8",   # output folder name
    workers=2,              # reduce if laptop lags
)

print("✅ Training complete! Check the 'runs/detect/helmet_yolov8' folder for results.")
