# Use an official Python image
FROM python:3.11-slim

# Set work directory
WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code
COPY . .

# Expose Django default port
EXPOSE 8000

# Run Django server
CMD ["python3", "manage.py", "runserver", "0.0.0.0:8000"]

