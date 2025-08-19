# -----------------------------
# Stage 1: Build stage (with compilers)
# -----------------------------
FROM python:3.13-slim AS builder

WORKDIR /app

# Install build tools for numpy/matplotlib
RUN apt-get update && apt-get install -y \
    build-essential \
    gcc \
    gfortran \
    libfreetype6-dev \
    libpng-dev \
    pkg-config \
    && rm -rf /var/lib/apt/lists/*

# Copy app and requirements
COPY requirements.txt .
COPY . .

# Install Python packages into a temporary location
RUN pip install --prefix=/install --no-cache-dir -r requirements.txt

# -----------------------------
# Stage 2: Final image (clean, small)
# -----------------------------
FROM python:3.13-slim

WORKDIR /app

# Install cron (no need for compilers in final image)
RUN apt-get update && apt-get install -y cron && rm -rf /var/lib/apt/lists/*

# Copy installed packages from builder
COPY --from=builder /install /usr/local

# Copy app files
COPY . /app

# Expose Flask port
EXPOSE 5000

# Add cron job: example daily at 6 AM
RUN echo "0 10 * * * root python /app/fetch_prices.py >> /var/log/cron.log 2>&1" >> /etc/crontab \
    && touch /var/log/cron.log

# Start cron + Flask app
CMD ["sh", "-c", "cron && python /app/dca.py"]
