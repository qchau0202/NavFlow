# NavFlow
Smart Traffic Congestion Prediction and Navigation using Camera Data in Ho Chi Minh City

## Hướng dẫn sử dụng data crawl lấy ảnh
```
B1: dùng commandprompt thay vì powershell -> cd vào data_crawl_demo -> tạo môi trường ảo: python -m venv venv
B2: chạy môi trường ảo venv -> venv\Scripts\activate.bat
B3: update pip -> python.exe -m pip install --upgrade pip
B4: tải packages -> pip install -r requirements.txt 
B5: xóa dataset cũ (nếu có)
B6: vào file data_crawl.py, kiểm tra số lượng ảnh muốn fetch cho mỗi cam ở dòng 91
    fetch bao nhiêu thì điền vô bấy nhiêu, mặc định đang để là 5
B7: chạy file -> python data_crawl.py
B8: lặp lại bước 6 nếu muốn lấy dataset từ đầu
B9: sau khi lấy data set xong -> venv\Scripts\deactivate.bat ( thoát môi trường ảo )
```