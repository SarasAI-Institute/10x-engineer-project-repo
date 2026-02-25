# Docker Configuration Documentation

This documentation provides detailed steps to build and run the FastAPI application using Docker. The setup leverages Docker and Docker Compose to streamline the development workflow.

## Prerequisites

- Ensure you have Docker and Docker Compose installed on your machine.
  - [Docker Installation Instructions](https://docs.docker.com/get-docker/)
  - [Docker Compose Installation Instructions](https://docs.docker.com/compose/install/)

## Dockerfile

The `Dockerfile` is used to build a Docker image for the FastAPI application. It utilizes a multi-stage build for efficiency:

### Key Parts of the Dockerfile:

- **Base Image**: Uses the Python 3.10 slim image for a smaller footprint.
- **Install Dependencies**: Installs Python dependencies in a separate build stage to keep the final image size small.
- **Application Code**: Copies only necessary files, ensuring a clean environment.
- **Expose Port**: Exposes port 8000 to communicate with the Uvicorn server.
- **Entrypoint**: Uses Uvicorn to serve the FastAPI application.

### Dockerfile

```Dockerfile
# Dockerfile

# Stage 1: Build stage
FROM python:3.10-slim as builder

WORKDIR /app

# Install dependencies
COPY backend/requirements.txt .
RUN pip install --user --no-cache-dir -r requirements.txt

# Stage 2: Production stage
FROM python:3.10-slim

WORKDIR /app

# Copy only the necessary parts from the builder
COPY --from=builder /root/.local /root/.local
ENV PATH=/root/.local/bin:$PATH

# Copy the application code
COPY backend /app

# Expose the application's port
EXPOSE 8000

# Run the application with Uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

## Docker Compose

**Docker Compose** helps manage and run multi-container Docker applications. Here, it is configured to handle only the app service for FastAPI.

### Key Features of `docker-compose.yml`:

- **Service Definition**: Defines a single `app` service that builds from the current directory using the Dockerfile.
- **Port Mapping**: Maps port 8000 of the container to port 8000 on the host machine for easy local development.

### docker-compose.yml

```yaml
# docker-compose.yml

version: '3.8'

services:
  app:
    build:
      context: .
      dockerfile: Dockerfile
    ports:
      - "8000:8000"
```

## Building and Running the Application

1. **Build the Docker Image**:
   Navigate to the project root (where the `Dockerfile` and `docker-compose.yml` are located) and build the Docker image:

   ```bash
   docker-compose build
   ```

2. **Run the Docker Container**:
   Start the application using Docker Compose:

   ```bash
   docker-compose up
   ```

3. **Accessing the Application**:
   Once the container is running, you can access your FastAPI application at `http://localhost:8000`. This URL serves the application via Uvicorn.

---

This setup simplifies the deployment process and ensures that your FastAPI application can be easily run in any environment that supports Docker. By following these steps, you provide a consistent environment that supports reproducibility and seamless application development or deployment.