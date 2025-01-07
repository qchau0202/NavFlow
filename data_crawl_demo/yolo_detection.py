import torch
import cv2
from PIL import Image
import numpy as np

# Load the YOLOv5 model
model = torch.hub.load('ultralytics/yolov5', 'yolov5s')

# Define the classes we are interested in
classes_of_interest = ['car', 'motorbike']

# Load an image
img_path = r'D:\Downloads\Projects\Test\NavFlow\data_crawl_demo\dataset\images\CMT8_1_Images\image_0.jpg'
img = Image.open(img_path)

# Perform inference
results = model(img)

# Filter results for cars and motorbikes
filtered_results = results.pandas().xyxy[0]
filtered_results = filtered_results[filtered_results['name'].isin(classes_of_interest)]

# Convert the image to OpenCV format
img_cv2 = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)

# Draw bounding boxes and labels on the image
for _, row in filtered_results.iterrows():
    x1, y1, x2, y2, conf, cls = int(row['xmin']), int(row['ymin']), int(row['xmax']), int(row['ymax']), row['confidence'], row['name']
    label = f"{cls} {conf:.2f}"
    cv2.rectangle(img_cv2, (x1, y1), (x2, y2), (0, 255, 0), 2)
    cv2.putText(img_cv2, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)

# Display the image
cv2.imshow('Image', img_cv2)
cv2.waitKey(0)
cv2.destroyAllWindows()
