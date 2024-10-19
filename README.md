# NavFlow
Smart Traffic Congestion Prediction and Navigation using Camera Data in Ho Chi Minh City

## Sử dụng data crawl lấy ảnh
```
B1: chạy môi trường ảo venv -> venv\Scripts\activate.bat
B2: update pip -> python.exe -m pip install -- upgrade pip
B3: tải packages -> pip install -r requirements.txt 
B4: xóa dataset cũ (nếu có)
B5: vào file data_crawl.py, kiểm tra số lượng ảnh muốn fetch cho mỗi cam ở dòng 91
    fetch bao nhiêu thì điền vô bấy nhiêu, mặc định đang để là 5
B6: chạy file -> python data_crawl.py
B7: lặp lại bước 4 nếu muốn lấy dataset từ đầu
```