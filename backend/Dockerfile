FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy application code
COPY app ./app
COPY requirements.txt ./

# Install dependencies
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# Expose port for the FastAPI app
EXPOSE 8000

# Default command to run the API
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
