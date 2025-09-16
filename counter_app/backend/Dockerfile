# Use a lightweight Python 3.9 image
FROM python:3.9-slim

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt .

# Install the Python dependencies
# The --no-cache-dir flag helps keep the image size down
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of your application code into the container
COPY . .

# Expose port 5000, which your Flask app runs on
EXPOSE 5000

# Command to run your Flask application
# This assumes your main Flask app file is named 'app.py'
# and the Flask app instance is named 'app' within that file.
CMD ["python", "app.py"]