# Stage 1: Build the Vue.js frontend
FROM node:14 as build-stage
WORKDIR /app/frontend
COPY frontend/package*.json ./

RUN npm install
COPY frontend/ .
RUN npm run build

# Stage 2: Setup the Python environment and copy the built frontend files
FROM python:3.9-slim
WORKDIR /app

# Install Python dependencies
COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the Flask application
COPY backend /app

# Copy the built static files from the Vue.js build stage
COPY --from=build-stage /app/frontend/dist /app/frontend/dist

# Expose the port Flask is accessible on
EXPOSE 5000

# Set environment variables
ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0

# Run the Flask application
CMD ["flask", "run"]
