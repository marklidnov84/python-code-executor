FROM ubuntu:22.04

# Install required packages
RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
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

# Install Python dependencies
COPY requirements.txt .
RUN pip3 install -r requirements.txt

# Clone and build nsjail
RUN git clone https://github.com/google/nsjail.git /nsjail && \
    cd /nsjail && \
    make && \
    mv /nsjail/nsjail /bin && \
    rm -rf /nsjail

# Create app directory
WORKDIR /app

# Copy application code
COPY . .

# Run as non-root user
RUN useradd -m myuser
USER myuser

# Start the application
CMD ["python3", "app.py"]