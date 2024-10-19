import requests, os, time, re, concurrent.futures
from datetime import datetime
from camera_api import CAMERA_URLS

# Lấy ảnh từ API
def fetch_camera_url(api_url, timeout=10):
    try:
        response = requests.get(api_url, timeout=timeout)  # Gửi req
        if response.status_code == 200:  # Kiểm tra req
            # Lấy camera id
            cam_id_match = re.search(r'"CamId":"(.*?)"', response.text)
            if cam_id_match:
                cam_id = cam_id_match.group(1) 
                # Lấy url theo từng cam
                return f"http://giaothong.hochiminhcity.gov.vn/render/ImageHandler.ashx?id={cam_id}"
    except requests.RequestException as error:
        print(f"Fetching camera failed: {error}")  
    return None

# Lưu ảnh theo path
def save_image(image_url, image_path, timeout=10):
    try:
        img_response = requests.get(image_url, timeout=timeout)  # Req để fetch ảnh
        if img_response.status_code == 200:  # Kiểm tra req
            with open(image_path, 'wb') as f:  # Mở file
                f.write(img_response.content)  # Viết file
                print(f"Saved: {image_path}")
            return True 
    except requests.RequestException as error:
        print(f"Error saving image: {error}") 
    return False

# Kiểm tra sự tồn tại của dir
def create_directory(directory):
    if not os.path.exists(directory):  
        os.makedirs(directory)  # Tạo dir mới
        print(f"Created directory: {directory}") 

# Lấy index của ảnh hiện tại
def get_next_image_index(camera_dir):
    # Kiểm tra có folder hay không
    if not os.path.exists(camera_dir):
        return 0
    # List ra các ảnh đã có
    existing_images = [f for f in os.listdir(camera_dir) if f.endswith('.jpg')]  # List all existing image files
    # Kiểm tra nếu không có ảnh
    if not existing_images:  
        return 0
    
    # Lấy số từ tên file (VD: 'image_1.jpg' -> 1)
    image_numbers = [int(re.search(r'image_(\d+)\.jpg', img).group(1)) for img in existing_images]
    return max(image_numbers) + 1  # Trả về index tiếp theo để lưu ảnh

# Chạy từng camera + lấy ảnh
def process_camera(camera_name, api_url, num_images, capture_interval=15):
    base_dir = "dataset/images"  # Folder lưu ảnh
    camera_dir = os.path.join(base_dir, f"{camera_name}_Images")  # Tạo folder to từng camera
    create_directory(camera_dir)  # Tạo folder nếu chưa có

    print(f"\nStarting fecthing for: {camera_name}")

    next_image_index = get_next_image_index(camera_dir)  # Lấy index ảnh tiếp theo
    images_captured = 0  # Biến đếm ảnh
    
    # Loop theo số lượng ảnh cần lấy ( biến num_images )
    while images_captured < num_images:
        camera_feed_url = fetch_camera_url(api_url)  # Lấy URL ảnh của camera
        if camera_feed_url:  # Kiểm tra đã lấy được chưa
            image_path = os.path.join(camera_dir, f"image_{next_image_index}.jpg")  # Tạo file ảnh + số ảnh
            if save_image(camera_feed_url, image_path):  
                images_captured += 1  # Tăng counter cho ảnh tiếp theo
                next_image_index += 1  # Tăng index qua ảnh tiếp theo
                time.sleep(capture_interval) # API reset mỗi 15s nên set interval = 15s, chỉnh lại cũng được
        else:
            print(f"Fetching URL failed for {camera_name}")  # Kiểm tra lỗi fetching của camera
            time.sleep(5) 
    print(f"Fecthing succeed: {num_images} images for {camera_name}")

def main():
    create_directory("dataset/images")

    max_cameras = len(CAMERA_URLS) # Tổng số camera 
    print(f"Starting capture with {max_cameras} concurrent cameras")  # In ra số lượng camera hiện có

    start_time = datetime.now()  # Ghi lại thời gian chạy (không có cũng được)

    # Dùng ThreadPoolExecutor để các camera chạy đồng thời (concurrently)
    with concurrent.futures.ThreadPoolExecutor(max_workers = max_cameras) as execute:
        latest = {
            #! Điền tham số cho hàm process_camera, lưu ý số lượng ảnh num_images
            execute.submit(process_camera, camera_name, api_url, num_images=5): camera_name
            for camera_name, api_url in CAMERA_URLS.items()
        }
        # Loop mỗi khi 1 camera thành công
        for get_cam in concurrent.futures.as_completed(latest):
            camera_name = latest[get_cam]  # Lấy tên camera được process gần nhất
            try:
                get_cam.result()
                print(f"Processing completed: {camera_name}")  
            except Exception as error:
                print(f"Processing failed: {camera_name}: {error}") 

    end_time = datetime.now()  # Thời gian hoàn thành
    duration = end_time - start_time 
    print(f"\nTotal time fetching: {duration}")
    print("Successfully!")

if __name__ == "__main__":
    main()
