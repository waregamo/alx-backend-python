# Use the required base image
FROM python:3.10

# Set working directory
WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copy the application source code
COPY . .

# Expose Django default port
EXPOSE 8000

# Start the Django app
CMD ["python3", "manage.py", "runserver", "0.0.0.0:8000"]

