# Use a base image with Chrome preinstalled
FROM python:3.10-slim

# Install Chrome
RUN apt-get update && \
    apt-get install -y wget unzip gnupg2 curl && \
    wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb && \
    apt install -y ./google-chrome-stable_current_amd64.deb && \
    rm google-chrome-stable_current_amd64.deb

# Set display port for Chrome
ENV DISPLAY=:99

# Set work directory
WORKDIR /app

# Copy files
COPY . /app

# Install Python dependencies
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Run your app
CMD ["gunicorn", "app:app", "--bind", "0.0.0.0:10000"]
