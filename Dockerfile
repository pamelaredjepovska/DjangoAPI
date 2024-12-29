# Use an official Python runtime as a parent image
FROM python:3.13.1

# The enviroment variable ensures that the python output is set straight
# to the terminal with out buffering it first
ENV PYTHONUNBUFFERED 1

# Create root directory for the project in the container
RUN mkdir /django_app

# Set the working directory to /django_app
WORKDIR /django_app

# Copy the current directory contents into the container at /django_app
ADD . /django_app/

# Copy the requirements file into the container
# COPY requirements.txt requirements.txt

# Install dependencies
RUN pip install --upgrade pip
RUN pip install --no-cache-dir --upgrade -r requirements.txt
