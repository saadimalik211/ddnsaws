FROM python:3.8-slim

# Set a directory for the app
WORKDIR /app

# Instead of copying everything, you only copy the 'app' directory from your project
COPY app/ .

# Install the dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Command to run the application
CMD ["python", "main.py"]

