# Base python image
FROM python:3.7-slim-buster

# Copy the code into a folder named app
ADD . /app

# switch the working directory to app
WORKDIR /app

# Install App dependencies
RUN pip3 install -r requirements.txt

# Set ENV variables
ENV PORT 5001

CMD ["python", "-u", "app.py"]