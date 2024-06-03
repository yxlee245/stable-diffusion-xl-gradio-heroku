FROM python:3.9.14-slim-buster

# Install tzdata for the missing timezone in ubuntu docker image; DEBIAN_FRONTEND for non-interactive installation
ENV DEBIAN_FRONTEND='noninteractive'

# Argument is passed in from docker-compose.yml file .e.g api
ARG SRC_PATH='.'

RUN apt-get -y update && \
    apt-get install -y --no-install-recommends \
    python3-dev \
    curl \
    build-essential \
    libmagic-dev \
    poppler-utils \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Setup permissions group and user under which the micro service will run
RUN groupadd -r nonroot &&\
    useradd -r -g nonroot -b /home -m nonroot && \
    usermod -aG sudo nonroot && \
    echo "nonroot ALL=(ALL) NOPASSWD:ALL" >> /etc/sudoers
USER nonroot

# Copy requirements from app and shared
COPY ${SRC_PATH}/requirements.txt /tmp/

# Always installed shared requirements first, since app may have dependencies that overwrite that
RUN pip3 install --no-cache-dir -U pip setuptools && pip3 install wheel
RUN pip3 install --no-cache-dir --user -r /tmp/requirements.txt

# Copy source code from microservice folder and the shared folder
COPY ${SRC_PATH}/src /home/nonroot/src
COPY ${SRC_PATH}/chatbot_app.py /home/nonroot/run.py

WORKDIR /home/nonroot
ENV PYTHONPATH /
ENV GRADIO_SERVER_NAME="0.0.0.0"

CMD python3 run.py
