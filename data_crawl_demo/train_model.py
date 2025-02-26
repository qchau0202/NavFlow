import os
import ultralytics
from ultralytics import YOLO

data_yaml = os.path.abspath("dataset/data.yaml")
model = YOLO("yolov8n.pt")
model.train(data="C:/Users/MSII/Desktop/NCKH/NavFlow/data_crawl_demo/dataset/data.yaml", 
            epochs=600, imgsz=640, device=0, batch = 8, workers = 0)
print("Training completed")
