# Use Python 3.10 as base image
FROM python:3.10-slim

# Set working directory in container
WORKDIR /app/src

# Copy requirements file
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire project
COPY . .

# Expose ports for API and Streamlit
EXPOSE 8000 8501

# Create script to run both services
RUN echo '#!/bin/bash\n\
python response_api.py &\n\
sleep 5\n\
streamlit run app.py' > ./start.sh

# Make the script executable
RUN chmod +x ./start.sh

# Copy .env file and set environment variables
ENV $(cat .env | xargs)

# Run the start script
CMD ["./start.sh"]