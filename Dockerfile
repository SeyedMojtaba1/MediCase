FROM docker.arvancloud.ir/python:3.12-slim

WORKDIR /app

# Configure mirrors with specific bookworm release
RUN rm -f /etc/apt/sources.list /etc/apt/sources.list.d/debian.sources && \
    echo 'deb https://mirror.iranserver.com/debian/ bookworm main contrib non-free' > /etc/apt/sources.list && \
    echo 'deb https://mirror.iranserver.com/debian/ bookworm-updates main contrib non-free' >> /etc/apt/sources.list && \
    echo 'deb https://mirror.iranserver.com/debian-security/ bookworm-security main contrib non-free' >> /etc/apt/sources.list

# IMPORTANT: Don't add bookworm-backports to avoid version conflicts
# If you need backports, install them separately with explicit versions

# Force apt to prefer stable versions and avoid mixed releases
RUN echo 'APT::Default-Release "bookworm";' > /etc/apt/apt.conf.d/01default-release && \
    echo 'Acquire::Check-Valid-Until "false";' > /etc/apt/apt.conf.d/99ignore-expiry

# Update and install packages with explicit bookworm release
RUN apt-get clean && \
    apt-get update && \
    apt-get install -y --no-install-recommends -t bookworm \
        gcc \
        default-libmysqlclient-dev \
        pkg-config \
        && rm -rf /var/lib/apt/lists/*

# Python deps (cached unless requirements.txt changes)
COPY requirements.txt .
RUN python -m venv /venv
ENV PATH="/venv/bin:$PATH"
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# App code (changes most frequently, placed last)
COPY MediCaseBack/ .

# Create non-root user for security (optional)
RUN useradd -m -u 1000 appuser && chown -R appuser:appuser /app
USER appuser

CMD ["gunicorn", "MediCaseBack.asgi:application", "-k", "uvicorn.workers.UvicornWorker", "--bind", "0.0.0.0:8000"]