FROM docker.arvancloud.ir/python:3.12-slim

WORKDIR /app

RUN if [ -f /etc/apt/sources.list.d/debian.sources ]; then \
        sed -i 's/deb.debian.org/mirror.iranserver.com/g' /etc/apt/sources.list.d/debian.sources; \
    fi && \
    if [ -f /etc/apt/sources.list ]; then \
        sed -i 's/deb.debian.org/mirror.iranserver.com/g' /etc/apt/sources.list; \
    fi

# 2. Tell apt to ignore expired release files
RUN echo 'Acquire::Check-Valid-Until "false";' > /etc/apt/apt.conf.d/99ignore-expiry

# 3. Clean, update (with the bypass flag just to be sure), and install
RUN apt-get clean && \
    apt-get -o Acquire::Check-Valid-Until=false update && \
    apt-get install -y \
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