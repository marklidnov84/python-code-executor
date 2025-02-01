FROM python:3.9-slim

# Install nsjail and dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    autoconf \
    bison \
    flex \
    gcc \
    g++ \
    git \
    libprotobuf-dev \
    libnl-route-3-dev \
    libtool \
    make \
    pkg-config \
    protobuf-compiler 
    
# Set up working directory
WORKDIR /app

RUN git clone https://github.com/google/nsjail.git && cd nsjail && make && mv nsjail /usr/local/bin && cd ..

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY app.py .

# Create necessary directories and set permissions
RUN mkdir -p /tmp/scripts && \
    chmod 777 /tmp/scripts && \
    chmod 755 /usr/local/bin/python3

# Expose port
EXPOSE 8080

# Run the application
CMD ["python", "app.py"]