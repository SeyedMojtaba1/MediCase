FROM docker.arvancloud.ir/python:3.12-slim

WORKDIR /app

# نصب پکیج‌های سیستمی
RUN apt-get update && apt-get install -y \
    gcc \
    default-libmysqlclient-dev \
    pkg-config \
    && rm -rf /var/lib/apt/lists/*

# ایجاد و فعال‌سازی همیشگی محیط مجازی
RUN python -m venv /venv
ENV PATH="/venv/bin:$PATH"

COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install -i https://mirror-pypi.runflare.com/ -r requirements.txt

# کپی کردن محتویات پوشه بک‌اند به داخل کانتینر
COPY MediCaseBack/ .

# این دستور صرفا برای دیباگ است و در کامپوز اورراید می‌شود
CMD ["gunicorn", "MediCaseBack.wsgi:application", "--bind", "0.0.0.0:8000"]