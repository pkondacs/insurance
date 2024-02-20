# Use a base image that contains the current stable Python version
FROM python:3.6

# Set the working directory in the container
WORKDIR /app
# Copy the current directory contents into the container at /app
COPY . /app

# Run any necessary commands to set up the environment or dependencies
# For example, if you have a requirements.txt file for a Python project:
RUN pip install --no-cache-dir -r requirements.txt

# Command to run when starting the container
CMD ["python3", "./files/main.py"]