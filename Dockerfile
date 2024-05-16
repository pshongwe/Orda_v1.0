# Setup the Python environment and copy the built frontend files
FROM python:3.9-slim
WORKDIR /app

# Install Python dependencies
COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the Flask application
COPY backend /app

# Expose the port Flask is accessible on
EXPOSE 5000

# Set environment variables
ENV GUNICORN_CMD_ARGS="--bind=0.0.0.0:5000 --workers=4 app:app"

# Run Gunicorn to serve Flask application
CMD ["gunicorn", "app:app"]
