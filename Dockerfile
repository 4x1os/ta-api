# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any necessary dependencies
RUN pip install -r requirements.txt

# Install Chrome and ChromeDriver for Selenium
RUN apt-get update && apt-get install -y \
    wget \
    unzip \
    libx11-dev \
    libdbus-1-3 \
    libxtst6 \
    chromium

# Set environment variables for Chrome
ENV CHROME_BIN=/usr/bin/chromium
ENV CHROME_DRIVER=/usr/bin/chromedriver

# Run the scraper script
CMD ["python", "scraper.py"]