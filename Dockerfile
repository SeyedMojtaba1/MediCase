FROM docker.arvancloud.ir/python:3.12-slim

WORKDIR /app

# Use Trixie mirrors instead of Bookworm
RUN rm -f /etc/apt/sources.list /etc/apt/sources.list.d/debian.sources && \
    echo 'deb https://mirror.iranserver.com/debian/ trixie main contrib non-free' > /etc/apt/sources.list && \
    echo 'deb https://mirror.iranserver.com/debian/ trixie-updates main contrib non-free' >> /etc/apt/sources.list && \
    echo 'deb https://mirror.iranserver.com/debian-security/ trixie-security main contrib non-free' >> /etc/apt/sources.list

# Or if trixie isn't available on the mirror, remove the default debian.org sources
RUN sed -i 's|deb.debian.org|mirror.iranserver.com/debian|g' /etc/apt/sources.list && \
    sed -i '/security.debian.org/d' /etc/apt/sources.list && \
    echo 'deb https://mirror.iranserver.com/debian-security/ trixie-security main' >> /etc/apt/sources.list

RUN echo 'Acquire::Check-Valid-Until "false";' > /etc/apt/apt.conf.d/99ignore-expiry

RUN apt-get clean && \
    apt-get update && \
    apt-get install -y --no-install-recommends \
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