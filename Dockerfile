FROM python:3.9-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Install the package
RUN pip install -e .

# Expose the port the app runs on
EXPOSE 3000

# Command to run the application
CMD ["python", "src/app.py"]
