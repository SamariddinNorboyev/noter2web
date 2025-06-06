# Use an official Python runtime as a parent image
FROM python:3.10-slim

# Set working directory inside container
WORKDIR /app

# Copy requirements file and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of your project code
COPY . .

# Expose the port your app runs on
EXPOSE 8000

# Command to run your app (change as per your project)
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
