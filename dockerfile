# 1. Use a modern, slim Python image for smaller size & speed
FROM python:3.11-slim

# 2. Set the working directory
WORKDIR /app

# 3. Install system build dependencies (required for ChromaDB/HNSWLib on slim images)
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# 4. Copy dependencies first (caching mechanism)
COPY requirements.txt .

# 5. Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# 6. Copy the rest of the application
COPY . .

# 7. Expose the port
EXPOSE 8000

# 8. Run the app without --reload (Production mode)
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]