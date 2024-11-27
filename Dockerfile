# Use an official Python runtime as a parent image
FROM python:3.12.2-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set the working directory
WORKDIR /app

# Install Git
RUN apt-get update && apt-get install -y git

# Install dependencies
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copy the current directory contents into the container
COPY . /app/

# Copy the .env file to the working directory
COPY .env /app/.env

# Collect static files
# RUN python manage.py collectstatic --noinput

# Make the migrations
# RUN python manage.py makemigrations

# Run migrations and start the Django application using Gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:80", "payday.wsgi:application"]
