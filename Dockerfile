FROM docker.arvancloud.ir/python:3.12-slim-bookworm

WORKDIR /app

# Configure apt to use Iran Server mirror for system packages
RUN rm -f /etc/apt/sources.list /etc/apt/sources.list.d/*.sources && \
    echo 'deb https://mirror.iranserver.com/debian/ bookworm main contrib non-free' > /etc/apt/sources.list && \
    echo 'deb https://mirror.iranserver.com/debian/ bookworm-updates main contrib non-free' >> /etc/apt/sources.list && \
    echo 'deb https://mirror.iranserver.com/debian-security/ bookworm-security main contrib non-free' >> /etc/apt/sources.list

RUN echo 'Acquire::Check-Valid-Until "false";' > /etc/apt/apt.conf.d/99ignore-expiry

# Install system dependencies
RUN apt-get clean && \
    apt-get update && \
    apt-get install -y --no-install-recommends \
        gcc \
        default-libmysqlclient-dev \
        pkg-config \
        && rm -rf /var/lib/apt/lists/*

# Copy pip configuration for Iran Server mirror
COPY pip.conf /etc/pip.conf

# Or for user-specific pip config (alternative location)
# RUN mkdir -p /root/.pip && COPY pip.conf /root/.pip/pip.conf

# Virtual environment
RUN python -m venv /venv
ENV PATH="/venv/bin:$PATH"

# Install Python dependencies using the local mirror
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY MediCaseBack/ .

CMD ["gunicorn", "MediCaseBack.asgi:application", "-k", "uvicorn.workers.UvicornWorker", "--bind", "0.0.0.0:8000"]