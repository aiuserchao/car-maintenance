# Use official Python slim image (small, secure, multi-arch)
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies (minimal build tools)
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Expose Streamlit port
EXPOSE 8501

# Configure Streamlit for headless operation (important for containers)
ENV STREAMLIT_SERVER_PORT=8501 \
    STREAMLIT_SERVER_ADDRESS=0.0.0.0 \
    STREAMLIT_SERVER_HEADLESS=true \
    STREAMLIT_SERVER_ENABLECORS=false \
    STREAMLIT_BROWSER_GATHER_USAGE_STATS=false

# Run the application
CMD ["streamlit", "run", "app.py"]
