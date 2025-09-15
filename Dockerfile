# Use an official Python runtime as a parent image
FROM python:3.11-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container at /app
COPY ./requirements.txt /app/requirements.txt

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt

# Copy the rest of the application's code into the container at /app
COPY ./app /app/app
COPY ./alembic /app/alembic
COPY ./alembic.ini /app/alembic.ini

# Expose the port the app runs on
EXPOSE 8000

# Run alembic upgrade head to apply migrations on startup
# Then, run uvicorn server
CMD alembic upgrade head && uvicorn app.main:app --host 0.0.0.0 --port 8000
