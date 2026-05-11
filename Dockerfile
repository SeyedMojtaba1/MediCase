FROM docker.arvancloud.ir/python:3.12-slim

WORKDIR /app

# Safer mirror replacement with fallback
RUN if [ -f /etc/apt/sources.list.d/debian.sources ]; then \
        sed -i 's|deb.debian.org|mirror.iranserver.com/debian|g' /etc/apt/sources.list.d/debian.sources && \
        sed -i 's|security.debian.org|mirror.iranserver.com/debian-security|g' /etc/apt/sources.list.d/debian.sources; \
    elif [ -f /etc/apt/sources.list ]; then \
        sed -i 's|http://deb.debian.org|https://mirror.iranserver.com/debian|g' /etc/apt/sources.list && \
        sed -i 's|http://security.debian.org|https://mirror.iranserver.com/debian-security|g' /etc/apt/sources.list; \
    else \
        echo 'deb https://mirror.iranserver.com/debian/ bookworm main contrib non-free' > /etc/apt/sources.list && \
        echo 'deb https://mirror.iranserver.com/debian/ bookworm-updates main contrib non-free' >> /etc/apt/sources.list && \
        echo 'deb https://mirror.iranserver.com/debian-security/ bookworm-security main contrib non-free' >> /etc/apt/sources.list; \
    fi

# Tell apt to ignore expired repository metadata timestamps
RUN echo 'Acquire::Check-Valid-Until "false";' > /etc/apt/apt.conf.d/99ignore-expiry

# Update and install compilation tools
RUN apt-get clean && \
    apt-get update && \
    apt-get install -y --no-install-recommends \
        gcc \
        default-libmysqlclient-dev \
        pkg-config \
        ca-certificates \
        && rm -rf /var/lib/apt/lists/*

# Virtual environment setup
RUN python -m venv /venv
ENV PATH="/venv/bin:$PATH"

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY MediCaseBack/ .

# Run the application
CMD ["gunicorn", "MediCaseBack.asgi:application", "-k", "uvicorn.workers.UvicronWorker", "--bind", "0.0.0.0:8000"]