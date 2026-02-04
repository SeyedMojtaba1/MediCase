FROM docker.arvancloud.ir/python:3.12-slim

WORKDIR /app

COPY requirements.txt .

RUN apt-get update && apt-get install -y \
    gcc \
    default-libmysqlclient-dev \
    pkg-config \
    && rm -rf /var/lib/apt/lists/*

RUN python -m venv /venv && /venv/bin/pip install --upgrade pip
RUN . /venv/bin/activate
RUN pip install -i https://pypi.jamko.ir/simple -r requirements.txt

COPY MediCaseBack/ .

CMD [ "ls", "/venv/bin/" ]