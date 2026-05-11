# Use explicit Bookworm version (stable) not Trixie (testing)
FROM docker.arvancloud.ir/python:3.12-slim-bookworm

WORKDIR /app

# Clean and configure ONLY Bookworm repositories
RUN rm -f /etc/apt/sources.list /etc/apt/sources.list.d/*.sources && \
    echo 'deb https://mirror.iranserver.com/debian/ bookworm main contrib non-free' > /etc/apt/sources.list && \
    echo 'deb https://mirror.iranserver.com/debian/ bookworm-updates main contrib non-free' >> /etc/apt/sources.list && \
    echo 'deb https://mirror.iranserver.com/debian-security/ bookworm-security main contrib non-free' >> /etc/apt/sources.list

# Configure apt to ignore expiry and fix potential issues
RUN echo 'Acquire::Check-Valid-Until "false";' > /etc/apt/apt.conf.d/99ignore-expiry && \
    echo 'APT::Get::Assume-Yes "true";' > /etc/apt/apt.conf.d/90assume-yes

# Update and install packages
RUN apt-get clean && \
    apt-get update && \
    apt-get install -y --no-install-recommends \
        gcc \
        default-libmysqlclient-dev \
        pkg-config \
        && apt-get clean \
        && rm -rf /var/lib/apt/lists/*

# Virtual environment
RUN python -m venv /venv
ENV PATH="/venv/bin:$PATH"

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY MediCaseBack/ .

CMD ["gunicorn", "MediCaseBack.asgi:application", "-k", "uvicorn.workers.UvicornWorker", "--bind", "0.0.0.0:8000"]