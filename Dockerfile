# Use an official Python runtime as a parent image
# python:3.11-slim-bullseye is a small, secure, and stable image
FROM python:3.11-slim-bullseye

# Set the working directory in the container
WORKDIR /usr/src/app

# Copy the requirements file into the working directory
COPY requirements.txt ./

# Install the dependencies with --trusted-host
RUN pip install --no-cache-dir --trusted-host pypi.org --trusted-host files.pythonhosted.org -r requirements.txt

# Copy the bot's code into the container
COPY bot.py .

# Define the command to run the application
CMD ["python", "bot.py"]
