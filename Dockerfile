# Use the official Python 3.11 slim image as the base image
FROM python:3.11-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt .

# Install the dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire application into the container
COPY . .

# Expose the port that the app runs on
EXPOSE 8080

# Run the FastAPI application on port 8080
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]

