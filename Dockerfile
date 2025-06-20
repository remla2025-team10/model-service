FROM python:3.12.9-slim AS builder

WORKDIR /app

# Install git and build tools incase of uncommon cpu architectures
RUN apt-get update && \
    apt-get install -y --no-install-recommends git build-essential && \
    rm -rf /var/lib/apt/lists/*

# Install dependencies
COPY requirements.txt .
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

FROM python:3.12.9-slim AS runtime

WORKDIR /model-service

# Copy the entire Python installation, including our newly installed packages
COPY --from=builder /usr/local /usr/local

# Copy the application code
COPY model-service/ .

EXPOSE 3000

CMD ["python", "app.py"]