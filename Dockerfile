# Stage 1: Build
FROM python:3.12-slim

# Set working directory
WORKDIR /app

# Copy application code
COPY . .

RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    software-properties-common \
    git \
    && rm -rf /var/lib/apt/lists/* \
    && pip install -r requirements.txt

# Expose Streamlit port
EXPOSE 8501

HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health

# Run Streamlit app
ENTRYPOINT ["streamlit", "run", "home.py", "--server.port=8501", "--server.address=0.0.0.0"]
