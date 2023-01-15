# Sets the base image for subsequent instructions
FROM python:3.8-slim-buster
# Copies the files to the working directory
COPY . /jikAPI
# Sets the working directory in the container  
WORKDIR /jikAPI
# Install dependencies
RUN pip install python-dotenv
RUN pip install --no-cache-dir -r requirements.txt
# Command to run on container start    
CMD ["flask", "run", "--host=0.0.0.0"]