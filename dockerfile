# Base Python image
FROM python:3.11-slim

# Install system dependencies (Tesseract and curl)
RUN apt-get update && \
    apt-get install -y tesseract-ocr libtesseract-dev wget curl && \
    rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy requirements and install Python packages
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy project code
COPY app/ ./app/

# Expose port
EXPOSE 8000

# Run the app
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
