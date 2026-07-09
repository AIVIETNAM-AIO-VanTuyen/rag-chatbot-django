# RAG Chatbot Django Project

Dự án RAG (Retrieval-Augmented Generation) Chatbot được phát triển bằng framework **Django** và sử dụng cơ sở dữ liệu **MySQL** chạy trên **Docker**.

---

## 📋 Yêu cầu hệ thống

Trước khi bắt đầu, hãy đảm bảo máy tính của bạn đã cài đặt các công cụ sau:

- **Python** (Phiên bản 3.10 trở lên)
- **Docker** và **Docker Compose**
- **Git** (để quản lý mã nguồn)

---

## 📁 Cấu trúc thư mục chính

```text
rag_chatbot_dijango/
├── rag_chatbot_dijango/    # Thư mục cấu hình dự án Django (settings, urls, wsgi...)
├── venv/                   # Môi trường ảo Python (Virtual Environment)
├── docker-compose.yml      # Cấu hình container MySQL cho Database
├── .env                    # Lưu trữ các biến môi trường cấu hình (Database, Port, v.v.)
├── requirements.txt        # Danh sách các thư viện Python cần thiết
└── manage.py               # Script quản lý dự án Django
```

---

## ⚙️ Hướng dẫn cài đặt và Chạy dự án

Dự án sử dụng cơ chế lai: **Database MySQL chạy trong Docker** và **Django App chạy trong môi trường ảo (venv) trên máy local**.

### Bước 1: Thiết lập cấu hình biến môi trường (`.env`)

Mở file `.env` ở thư mục gốc của dự án và đảm bảo các thông số chính xác:

```env
# Cấu hình Database MySQL
DB_NAME=rag_chatbot
DB_USER=admin@gmail.com
DB_PASSWORD=12345678
DB_ROOT_PASSWORD=root_password

# Đặt '127.0.0.1' nếu chạy Django trực tiếp trên máy local (ngoài Docker)
# Đặt 'db' nếu sau này đóng gói toàn bộ Django App vào Docker
DB_HOST=127.0.0.1
DB_PORT=3306
```

---

### Bước 2: Khởi động Database bằng Docker

Chạy lệnh sau tại thư mục gốc của dự án để khởi động container chứa MySQL Database ở chế độ chạy ngầm (detached mode):

```bash
docker compose up -d
```

> **Lưu ý:** Nếu bạn đang dùng phiên bản Docker cũ, lệnh có thể là `docker-compose up -d`.

Để kiểm tra trạng thái hoạt động của các container:

```bash
docker ps
```

Bạn sẽ thấy hai container đang chạy:

1. `rag_chatbot_db` (MySQL Database - cổng `3306`)
2. `rag_chatbot_phpmyadmin` (phpMyAdmin - cổng `8080`)

#### 🖥️ Quản lý Database qua Trình duyệt Web (phpMyAdmin)

Sau khi chạy Docker Compose, bạn có thể truy cập công cụ quản lý cơ sở dữ liệu qua trình duyệt web:

- **Địa chỉ:** [http://localhost:8080/](http://localhost:8080/)
- **Thông tin đăng nhập (lấy từ `.env`):**
  - **Server:** `db`
  - **Username:** `root` (hoặc `admin@gmail.com`)
  - **Password:** `root_password` (hoặc `12345678` tương ứng)

---

### Bước 3: Cài đặt và Chạy Django App trên Môi trường ảo

#### 1. Kích hoạt môi trường ảo (`venv`)

- **Trên Windows (PowerShell):**
  ```powershell
  .\venv\Scripts\Activate.ps1
  ```
- **Trên Windows (Command Prompt - CMD):**
  ```cmd
  venv\Scripts\activate.bat
  ```
- **Trên Linux / macOS:**
  ```bash
  source venv/bin/activate
  ```

#### 2. Cài đặt các thư viện phụ thuộc

Cài đặt các thư viện đã được cấu hình trong `requirements.txt` bằng lệnh:

```bash
pip install -r requirements.txt
```

_Lưu ý cho môi trường Windows:_ Thư viện `mysqlclient` yêu cầu công cụ biên dịch C++ của Microsoft. Nếu gặp lỗi cài đặt, bạn có thể cài đặt package whl thích hợp hoặc chuyển sang dùng thư viện thay thế là `pymysql` (cần khai báo trong `__init__.py`).

#### 3. Thực hiện chuyển đổi cấu trúc Database (Migrations)

Để tạo các bảng cơ sở dữ liệu mặc định của Django trong container MySQL:

```bash
python manage.py migrate
```

#### 4. Khởi động server phát triển (Development Server)

Chạy lệnh:

```bash
python manage.py runserver
```

Server sẽ khởi động tại địa chỉ: [http://127.0.0.1:8000/](http://127.0.0.1:8000/)

---

## 🛠️ Một số lệnh hữu ích khác

- **Tạo tài khoản quản trị (Superuser):**
  ```bash
  python manage.py createsuperuser
  ```
- **Tạo file migrations mới sau khi chỉnh sửa Model:**
  ```bash
  python manage.py makemigrations
  ```
- **Dừng container Database:**
  ```bash
  docker compose down
  ```
- **Dừng container Database và xóa toàn bộ dữ liệu đã lưu:**
  ```bash
  docker compose down -v
  ```
