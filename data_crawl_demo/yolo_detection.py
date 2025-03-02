import os
import time
import re
import requests
import cv2
import numpy as np
import concurrent.futures
from datetime import datetime
from queue import Queue
from threading import Thread
from typing import Optional, Dict
from ultralytics import YOLO
from camera_api import CAMERA_URLS


# Load model YOLOv8 đã train
print("Starting program...")
MODEL_PATH = r"C:\Users\MSII\Desktop\NCKH\NavFlow\runs\detect\train\weights\best.pt"
print(f"Loading model from {MODEL_PATH}...")
model = YOLO(MODEL_PATH)
print("Model loaded successfully!")
print("Starting detection...")


class CameraCapture:
    def __init__(self, frame_queue: Queue):
        self.session = requests.Session()
        self.frame_queue = frame_queue  # Hàng đợi để gửi ảnh cho YOLO
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0',
            'Accept': 'image/avif,image/webp,image/apng,*/*',
            'Referer': 'http://giaothong.hochiminhcity.gov.vn/',
        })

    def create_folder_structure(self, camera_name: str) -> str:
        camera_dir = os.path.join("detections", camera_name)
        os.makedirs(camera_dir, exist_ok=True)
        return camera_dir

    def fetch_camera_image(self, api_url: str, timeout: int = 1) -> Optional[np.ndarray]:
        try:
            cam_id_match = re.search(r'camId=([^&]+)', api_url)
            if cam_id_match:
                cam_id = cam_id_match.group(1)
                image_url = f"http://giaothong.hochiminhcity.gov.vn/render/ImageHandler.ashx?id={cam_id}"
                img_response = self.session.get(image_url, timeout=timeout, stream=True)
                
                if img_response.status_code == 200 and img_response.headers.get('content-type', '').startswith('image/'):
                    img_array = np.asarray(bytearray(img_response.content), dtype=np.uint8)
                    frame = cv2.imdecode(img_array, cv2.IMREAD_COLOR)
                    if frame is None:
                        print("Failed to decode image!")
                    return frame    
                
        except requests.RequestException as error:
            print(f"Error accessing image URL: {error}")
        return None

    def process_camera(self, camera_name: str, api_url: str, num_images: int, capture_interval: int = 15):
        print(f"\nStarting capture for: {camera_name}")
        images_captured = 0
        while images_captured < num_images:
            frame = self.fetch_camera_image(api_url)
            if frame is not None:
                # Đưa ảnh vào hàng đợi để YOLO xử lý
                print(f"Captured image for {camera_name}, sending to queue...")
                self.frame_queue.put((camera_name, frame))
                print(f"Image sent to YOLO for processing: {camera_name}")
                images_captured += 1
            time.sleep(capture_interval)

def detect_objects(frame_queue: Queue):
    while True:
        print("Waiting for frame...")
        camera_name, frame = frame_queue.get()
        
        # Chạy YOLO detect
        results = model(frame)

        # Tính toán độ đầy của đường
        fullness = calculate_fullness(frame, results)

        # Lưu ảnh kết quả vào detections/tênCamera/
        save_detection_results(camera_name, frame, results, fullness)
def calculate_fullness(frame: np.ndarray, results) -> float:
    frame_area = frame.shape[0] * frame.shape[1]
    vehicle_area = 0

    for r in results:
        for box in r.boxes:
            x1, y1, x2, y2 = map(int, box.xyxy[0])
            vehicle_area += (x2 - x1) * (y2 - y1)

    fullness = (vehicle_area / frame_area) * 100
    return fullness

def save_detection_results(camera_name: str, frame: np.ndarray, results, fullness: float):
    output_dir = os.path.join("detections", camera_name)
    os.makedirs(output_dir, exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_path = os.path.join(output_dir, f"{timestamp}.jpg")
    data_path = os.path.join(output_dir, "data.txt")

    with open(data_path, "a") as data_file:
        data_file.write(f"Timestamp: {timestamp}\n")
        data_file.write(f"Fullness of the road: {fullness:.2f}%\n")
        data_file.write("Detected objects:\n")

        for r in results:
            for box in r.boxes:
                x1, y1, x2, y2 = map(int, box.xyxy[0])
                confidence = box.conf[0].item()
                label = model.names[int(box.cls[0])]

                # Vẽ bounding box + label
                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                cv2.putText(frame, f"{label} {confidence:.2f}", 
                            (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 
                            0.5, (0, 255, 0), 2)

                data_file.write(f"  - {label}: {confidence:.2f} (bbox: {x1}, {y1}, {x2}, {y2})\n")

        data_file.write("\n")

    # Lưu ảnh kết quả vào thư mục detections/tênCamera/
    cv2.imwrite(output_path, frame)
    print(f"Detection result saved: {output_path}")
    print(f"Fullness of the road: {fullness:.2f}%")

def main(camera_urls: Dict[str, str], num_images: int = 5):
    frame_queue = Queue(maxsize=10)
    capture = CameraCapture(frame_queue=frame_queue)

    # Chạy YOLO detection song song
    yolo_thread = Thread(target=detect_objects, args=(frame_queue,), daemon=True)
    yolo_thread.start()

    with concurrent.futures.ThreadPoolExecutor(max_workers=len(camera_urls)) as executor:
        for camera_name, api_url in camera_urls.items():
            executor.submit(capture.process_camera, camera_name, api_url, num_images)
            
if __name__ == "__main__":
    main(CAMERA_URLS, num_images=2)

