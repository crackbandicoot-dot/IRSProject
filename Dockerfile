# Use an official Python runtime as a parent image
FROM python:3.13-slim

# Set the working directory in the container
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy the requirements file into the container
COPY requirements.txt .

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . .

# Create a startup script
RUN echo '#!/bin/bash\n\
echo "Waiting for databases to be ready..."\n\
sleep 10\n\
\n\
echo "Initializing MongoDB..."\n\
python Scripts/create_db.py --connection "$MONGODB_URI" --data-file _\n\
\n\
echo "Initializing Qdrant..."\n\
python Scripts/create_vector_db.py --host "$QDRANT_HOST" --port "$QDRANT_PORT"\n\
\n\
echo "Starting Crawler Pipeline..."\n\
python crawler_pipeline.py\n\
\n\
echo "Starting Web Application..."\n\
python main.py' > /app/start.sh && chmod +x /app/start.sh

# Expose the port the app runs on
EXPOSE 5000

# Run the startup script
CMD ["/app/start.sh"]
