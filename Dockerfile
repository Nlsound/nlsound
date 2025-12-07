# Use a slim Python base image
FROM python:3.11-slim

# Ensure Python output is sent straight to terminal without buffering
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    # Flask app entry point
    FLASK_APP=app.py \
    # Fly.io wants apps to listen on 0.0.0.0:8080
    PORT=8080

# Set working directory
WORKDIR /app

# System dependencies (if needed for building wheels)
RUN apt-get update && \
    apt-get install -y --no-install-recommends build-essential && \
    rm -rf /var/lib/apt/lists/*

# Copy requirement spec first for caching
COPY requirements.txt ./

# Install dependencies
RUN pip install --upgrade pip && \
    pip install -r requirements.txt

# Copy the rest of the application
COPY . .

# Expose the port that the app will run on
EXPOSE 8080

# Healthcheck (simple TCP check)
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
  CMD python -c "import socket,os; s=socket.socket(); s.settimeout(2); s.connect(('127.0.0.1', int(os.environ.get('PORT', '8080')))); s.close()" || exit 1

# Start the app with gunicorn, binding to 0.0.0.0:8080
# 'app:app' refers to the module 'app.py' and the Flask instance 'app'
CMD ["gunicorn", "--bind", "0.0.0.0:8080", "--workers", "2", "--threads", "4", "--timeout", "60", "app:app"]
