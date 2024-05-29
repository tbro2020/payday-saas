# syntax=docker/dockerfile:1
FROM python:3.12.2
WORKDIR /app

# Upgrade pip and install required packages
RUN pip install --upgrade pip
ADD ./requirements.txt /app/
RUN pip install -r requirements.txt

# Install gunicorn separately to avoid version conflicts
RUN pip install gunicorn

# Copy the application code
ADD . /app

# Make the entrypoint scripts executable
RUN chmod +x /app/server-entrypoint.sh
RUN chmod +x /app/worker-entrypoint.sh

# Set the entrypoint for the server
ENTRYPOINT ["/app/server-entrypoint.sh"]

