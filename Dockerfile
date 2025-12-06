# --- Base Image ---
FROM python:3.11-slim

# --- Set working directory ---
WORKDIR /app

# --- Install system dependencies for Python packages ---
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# --- Copy project files ---
COPY . .

# --- Install Python dependencies ---
RUN pip install --no-cache-dir -r requirements.txt

# --- Expose PORT (Fly will use this) ---
ENV PORT=8080
EXPOSE 8080

# --- Launch application using Gunicorn ---
CMD ["gunicorn", "-b", "0.0.0.0:8080", "app:app"]
