import requests
import os
import time
import re
import concurrent.futures
from datetime import datetime
from typing import Optional, Dict
from urllib.parse import quote

class CameraCapture:
    def __init__(self, base_dir: str = "dataset/images"):  # Changed back to dataset/images
        self.base_dir = base_dir
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'Accept-Language': 'en-US,en;q=0.9',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Cache-Control': 'max-age=0',
            'Referer': 'http://giaothong.hochiminhcity.gov.vn/',
        })

    def create_folder_structure(self, camera_name: str) -> str:
        # Create camera-specific directory under existing base_dir
        camera_dir = os.path.join(self.base_dir, camera_name)
        if not os.path.exists(camera_dir):
            os.makedirs(camera_dir)
            print(f"Created camera directory: {camera_dir}")
        
        return camera_dir

    def fetch_camera_url(self, api_url: str, timeout: int = 1) -> Optional[str]:
        try:
            cam_id_match = re.search(r'camId=([^&]+)', api_url)
            if cam_id_match:
                cam_id = cam_id_match.group(1)
                image_url = f"http://giaothong.hochiminhcity.gov.vn/render/ImageHandler.ashx?id={cam_id}"
                
                img_response = self.session.get(image_url, timeout=timeout)
                if img_response.status_code == 200:
                    content_type = img_response.headers.get('content-type', '')
                    if content_type.startswith('image/'):
                        return image_url
                    print(f"Invalid content type received: {content_type}")
                else:
                    print(f"Image URL returned status code: {img_response.status_code}")
            else:
                print("Failed to extract camera ID from URL")
                
        except requests.RequestException as error:
            print(f"Error accessing image URL: {error}")
        except Exception as error:
            print(f"Unexpected error: {error}")
        return None

    def save_image(self, image_url: str, image_path: str, timeout: int = 1) -> bool:
        max_retries = 5
        for attempt in range(max_retries):
            try:
                if attempt > 0:
                    time.sleep(2)

                img_response = self.session.get(
                    image_url, 
                    timeout=timeout,
                    stream=True
                )
                img_response.raise_for_status()
                
                content_type = img_response.headers.get('content-type', '')
                if not content_type.startswith('image/'):
                    print(f"Warning: Unexpected content type: {content_type}")
                    continue

                with open(image_path, 'wb') as f:
                    for chunk in img_response.iter_content(chunk_size=8192):
                        if chunk:
                            f.write(chunk)
                
                if os.path.exists(image_path) and os.path.getsize(image_path) > 0:
                    print(f"Successfully saved: {image_path}")
                    return True
                else:
                    print(f"File saved but may be empty: {image_path}")
                    
            except requests.RequestException as error:
                print(f"Attempt {attempt + 1}/{max_retries} failed: {error}")
                
        return False

    def process_camera(self, camera_name: str, api_url: str, num_images: int, capture_interval: int = 15):
        # Create folder structure for this camera
        camera_dir = self.create_folder_structure(camera_name)
        print(f"\nStarting capture for: {camera_name}")
        next_image_index = self.get_next_image_index(camera_dir)
        images_captured = 0
        consecutive_failures = 0
        max_failures = 5
        while images_captured < num_images and consecutive_failures < max_failures:
            try:
                actual_interval = capture_interval + (time.time() % 2)                
                camera_feed_url = self.fetch_camera_url(api_url)
                if camera_feed_url:
                    image_path = os.path.join(camera_dir, f"image_{next_image_index}.jpg")
                    if self.save_image(camera_feed_url, image_path):
                        images_captured += 1
                        next_image_index += 1
                        consecutive_failures = 0
                        time.sleep(actual_interval)
                    else:
                        consecutive_failures += 1
                        time.sleep(5)
                else:
                    consecutive_failures += 1
                    time.sleep(5)
            except Exception as error:
                consecutive_failures += 1
                print(f"Error processing {camera_name}: {error}")
                time.sleep(5)

        if consecutive_failures >= max_failures:
            print(f"Stopped capturing {camera_name} due to too many failures")
        else:
            print(f"Successfully captured {images_captured} images for {camera_name}")

    def get_next_image_index(self, camera_dir: str) -> int:
        try:
            existing_images = [f for f in os.listdir(camera_dir) if f.endswith('.jpg')]
            if not existing_images:
                return 0   
            image_numbers = []
            for img in existing_images:
                match = re.search(r'image_(\d+)\.jpg', img)
                if match:
                    image_numbers.append(int(match.group(1)))
            return max(image_numbers + [-1]) + 1
        except Exception as error:
            print(f"Error getting next image index: {error}")
            return 0

def main(camera_urls: Dict[str, str], num_images: int = 2):
    # Check if base directory exists, create only if it doesn't
    base_dir = "dataset/images"
    if not os.path.exists(base_dir):
        os.makedirs(base_dir)
        print(f"Created base directory: {base_dir}")
    else:
        print(f"Using existing base directory: {base_dir}")
    capture = CameraCapture(base_dir)
    print(f"Starting concurrent capture for {len(camera_urls)} cameras")
    start_time = datetime.now()
    with concurrent.futures.ThreadPoolExecutor(max_workers=len(camera_urls)) as executor:
        # Create a map of futures to camera names
        future_to_camera = {
            executor.submit(capture.process_camera, camera_name, api_url, num_images): camera_name 
            for camera_name, api_url in camera_urls.items()
        }
        # Process completed futures as they finish
        for future in concurrent.futures.as_completed(future_to_camera):
            camera_name = future_to_camera[future]
            try:
                future.result()  # Get the result or raise any exceptions
                print(f"Completed processing: {camera_name}")
            except Exception as error:
                print(f"Failed processing {camera_name}: {error}")
    duration = datetime.now() - start_time
    print(f"\nTotal capture time: {duration}")
    print("Capture completed")

if __name__ == "__main__":
    # Example camera URLs
    from camera_api import CAMERA_URLS
    main(CAMERA_URLS, num_images=1)