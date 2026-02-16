FROM docker.arvancloud.ir/python:3.12-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    gcc \
    default-libmysqlclient-dev \
    pkg-config \
    && rm -rf /var/lib/apt/lists/*

RUN python -m venv /venv
ENV PATH="/venv/bin:$PATH"

COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install -i https://mirror-pypi.runflare.com/ -r requirements.txt

COPY MediCaseBack/ .

CMD ["gunicorn", "MediCaseBack.wsgi:application", "--bind", "0.0.0.0:8000"]