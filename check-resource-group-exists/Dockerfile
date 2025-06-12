FROM python:3.11-slim

# Set work directory
WORKDIR /app

# Copy requirements.txt first (for better Docker caching)
COPY requirements.txt .

# Install dependencies from requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of your action code
COPY . .

# Set the entrypoint
ENTRYPOINT ["python", "/app/entrypoint.py"]