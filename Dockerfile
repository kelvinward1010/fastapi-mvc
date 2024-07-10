
FROM python:3.9

# Thiết lập thư mục làm việc trong container
WORKDIR /app

# Sao chép file requirements.txt vào thư mục /app
COPY ./requirements.txt /app/requirements.txt

# Cài đặt các dependencies từ requirements.txt
RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt

# Sao chép toàn bộ mã nguồn ứng dụng vào thư mục /app
COPY ./app /app/app

# Chạy ứng dụng FastAPI với Uvicorn trên cổng 80
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "1010"]
