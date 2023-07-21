# We will use python:3.10-alpine as the base image for building the Flask container
FROM python:3.10-alpine
# Upgrade pip to the latest version
RUN pip install --upgrade pip
# It specifies the working directory where the Docker container will run
WORKDIR /app
# Copying all the application files to the working directory
COPY . .
# Install all the dependencies required to run the Flask application
RUN pip install -r requirements.txt
# Expose the Docker container for the application to run on port 5000
EXPOSE 5000
# The command required to run the Dockerized application
CMD ["python", "/app/app.py"]
