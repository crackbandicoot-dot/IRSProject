# Use an official Python runtime as a parent image
FROM python:3.13-slim

# Set the working directory in the container
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy the requirements file into the container
COPY requirements.txt .

# Install any needed packages specified in requirements.txt
# Remove windows specific packages that won't install on Linux
RUN sed -i '/pywin32/d' requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . .

# Patch hardcoded localhost for Docker (without changing the workspace files)
RUN sed -i 's/localhost:27017/mongodb:27017/g' document_repository/document_repository_impl.py || true
RUN sed -i 's/localhost:27017/mongodb:27017/g' index_repository/index_repository_impl.py || true
RUN sed -i 's/"localhost"/"qdrant"/g' document_embedding_repository/document_embedding_repository_impl.py || true

# Create a startup script
RUN echo '#!/bin/bash\n\
echo "Waiting for MongoDB and Qdrant to be ready..."\n\
sleep 10\n\
\n\
echo "Initializing MongoDB..."\n\
python Scripts/create_db.py --connection mongodb://mongodb:27017/ --data-file _\n\
\n\
echo "Initializing Qdrant..."\n\
python Scripts/create_vector_db.py --host qdrant --port 6333\n\
\n\
echo "Starting Crawler Pipeline (this may take a while, 2500 pages)..."\n\
python crawler_pipeline.py\n\
\n\
echo "Crawler finished. Starting Web Application..."\n\
python main.py' > /app/start.sh && chmod +x /app/start.sh

# Expose the port the app runs on
EXPOSE 5000

# Run the startup script
CMD ["/app/start.sh"]
