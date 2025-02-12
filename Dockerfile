# Use the official Python image
FROM python:3.10

# Set the working directory
WORKDIR /app

# Copy project files to the container
COPY Gluroo2Nightscout.py .  
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Run the script
CMD ["python", "Gluroo2Nightscout.py"]
