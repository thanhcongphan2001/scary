import json

file_path = "lat_lon_q1.txt"
with open(file_path, 'r') as text_file:
    lines = text_file.read()
    
result_list = []

for line in lines.split('\n'):
    if line.strip():  # Đảm bảo không xử lý các dòng trống
        lat, lon = map(float, line.split())
        result_list.append({"lat": lat, "lon": lon})
print("độ dài của mảng",len(result_list))
file_path = "lat_lon_q1.json"
with open(file_path, 'w') as json_file:
    json.dump(result_list, json_file,indent=4)

with open(file_path, 'r') as json_file:
    data = json.load(json_file)
# Hiển thị dữ liệu
# print("adsd",data)