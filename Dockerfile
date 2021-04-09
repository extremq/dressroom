# Using official python runtime base image
FROM python:3.7-slim

# Set the application directory
WORKDIR /src

# Install git
RUN apt-get update
RUN apt-get install -y git

# Install our requirements.txt
COPY requirements.txt /src/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Unpack assets
COPY packed-assets /src/packed-assets
RUN python -u packed-assets/unpack.py

# Copy our code from the current folder to /src inside the container
COPY . .

# Define our command to be run when launching the container
CMD ["python", "-u", "service.py"]