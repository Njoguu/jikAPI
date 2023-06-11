# Sets the base image for subsequent instructions
FROM python:3.12.0b2-slim-bullseye

# Sets the working directory in the container  
WORKDIR /jikAPI

# Copies the files to the working directory
COPY . /jikAPI

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Command to run on container start    
CMD ["flask", "run", "--host=0.0.0.0"]