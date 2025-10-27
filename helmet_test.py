from ultralytics import YOLO

# Load pretrained helmet detection model
model = YOLO("C:/Users/megha/Downloads/basic_project/HelmetDetectionYolo/weights/best.pt")

# Run prediction on test image
model.predict(source="C:/Users/megha/Downloads/basic_project/HelmetDetectionYolo/data/images/test", show=True, save=True)
