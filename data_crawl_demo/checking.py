# import torch
# print(torch.cuda.is_available())  # Kiểm tra CUDA đã hoạt động chưa
# print(torch.cuda.device_count())  # Kiểm tra số GPU
# print(torch.version.cuda)  # Kiểm tra phiên bản CUDA mà PyTorch nhận

# import os

# label_path = "C:/Users/MSII/Desktop/NCKH/NavFlow/data_crawl_demo/dataset/labels/train"
# for file in os.listdir(label_path):
#     with open(os.path.join(label_path, file), "r") as f:
#         lines = f.readlines()
#         for line in lines:
#             data = line.strip().split()
#             if len(data) > 5:  # Nếu có hơn 5 giá trị, có thể chứa segment
#                 print(f"Lỗi dữ liệu ở file: {file}, nội dung: {line}")
                
# import os

# label_path = "C:/Users/MSII/Desktop/NCKH/NavFlow/data_crawl_demo/dataset/labels/train"

# for file in os.listdir(label_path):
#     file_path = os.path.join(label_path, file)
    
#     with open(file_path, "r") as f:
#         lines = f.readlines()
    
#     new_lines = []
#     for line in lines:
#         data = line.strip().split()
#         if len(data) == 5:
#             new_lines.append(line)
    
#     with open(file_path, "w") as f:
#         f.writelines(new_lines)

# print("Deleted")
