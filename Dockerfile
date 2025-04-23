# Base image
FROM python:3.12-slim

# Install system dependencies for running Chrome and Chromedriver
RUN apt-get update -y && apt-get install -y \
    wget \
    curl \
    unzip \
    ca-certificates \
    fonts-liberation \
    libappindicator3-1 \
    libgdk-pixbuf2.0-0 \
    libnspr4 \
    libnss3 \
    xdg-utils \
    --no-install-recommends \
    && apt-get clean

# Install Chrome (stable version)
RUN curl -sS https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb -o chrome.deb
RUN dpkg -i chrome.deb || apt-get -y -f install

# Install Chromedriver
RUN CHROMEDRIVER_VERSION=`curl -sS chromedriver.storage.googleapis.com/LATEST_RELEASE` \
    && wget https://chromedriver.storage.googleapis.com/${CHROMEDRIVER_VERSION}/chromedriver_linux64.zip \
    && unzip chromedriver_linux64.zip \
    && mv chromedriver /usr/local/bin/ \
    && chmod +x /usr/local/bin/chromedriver

# Set working directory inside container
WORKDIR /app

# Copy your project files into the container
COPY . /app

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Run your bot when the container starts
CMD ["python", "bot.py"]
