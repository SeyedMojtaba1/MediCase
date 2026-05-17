FROM docker.arvancloud.ir/python:3.12-slim-bookworm

WORKDIR /app

# Remove any existing pip config files
RUN rm -f /etc/pip.conf /root/.pip/pip.conf

# Configure pip to use Iran Server mirror
# RUN pip config set global.index-url https://pypi.iranserver.com/repository/pypi/simple && \
# RUN pip config set global.index-url https://mirror-pypi.runflare.com/simple && \
#     pip config set global.trusted-host pypi.iranserver.com && \
#     pip config set global.timeout 60

# Configure apt to use Iran Server mirror
RUN rm -f /etc/apt/sources.list && \
    echo 'deb https://mirror.iranserver.com/debian/ bookworm main contrib non-free' > /etc/apt/sources.list && \
    echo 'deb https://mirror.iranserver.com/debian/ bookworm-updates main contrib non-free' >> /etc/apt/sources.list && \
    echo 'deb https://mirror.iranserver.com/debian-security/ bookworm-security main contrib non-free' >> /etc/apt/sources.list && \
    echo 'Acquire::Check-Valid-Until "false";' > /etc/apt/apt.conf.d/99ignore-expiry

# Update and install packages
RUN apt-get clean && \
    apt-get update && \
    apt-get install -y --no-install-recommends \
        gcc \
        default-libmysqlclient-dev \
        pkg-config \
        && rm -rf /var/lib/apt/lists/*

# Virtual environment setup
RUN python -m venv /venv
ENV PATH="/venv/bin:$PATH"

# Install Python dependencies
COPY requirements.txt .
RUN pip install --upgrade pip -i https://pypi.iranserver.com/repository/pypi/simple
RUN pip install -r requirements.txt \
    -i https://pypi.iranserver.com/repository/pypi/simple \
    --extra-index-url https://mirror-pypi.runflare.com/simple \
    --extra-index-url https://icodeacademy.ir/python-packages \
    --extra-index-url https://archive.ito.gov.ir/mirror2/python/simple

COPY MediCaseBack/ .

CMD ["gunicorn", "MediCaseBack.asgi:application", "-k", "uvicorn.workers.UvicornWorker", "--bind", "0.0.0.0:8000"]