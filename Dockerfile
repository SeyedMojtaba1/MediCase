FROM docker.arvancloud.ir/python:3.12-slim

WORKDIR /app

RUN sed -i 's|deb.debian.org|mirror.iranserver.com/debian|g' /etc/apt/sources.list.d/debian.sources && \
    sed -i 's|security.debian.org|mirror.iranserver.com/debian-security|g' /etc/apt/sources.list.d/debian.sources

# 2. Tell apt to ignore expired repository metadata timestamps (crucial for local mirror syncs)
RUN echo 'Acquire::Check-Valid-Until "false";' > /etc/apt/apt.conf.d/99ignore-expiry

# 3. Update the indexes and install the compilation tools
RUN apt-get clean && \
    apt-get -o Acquire::Check-Valid-Until=false update && \
    apt-get install -y --no-install-recommends \
        gcc \
        default-libmysqlclient-dev \
        pkg-config \
        && rm -rf /var/lib/apt/lists/*

RUN python -m venv /venv
ENV PATH="/venv/bin:$PATH"

COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

COPY MediCaseBack/ .

CMD ["gunicorn", "MediCaseBack.asgi:application", "-k", "uvicorn.workers.UvicornWorker", "--bind", "0.0.0.0:8000"]