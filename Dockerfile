# Use the official lightweight Python image.
# https://hub.docker.com/_/python
FROM python:3.10-slim

# Allow statements and log messages to immediately appear in the Knative logs
ENV PYTHONUNBUFFERED True

ENV APP_HOME /app
WORKDIR $APP_HOME

# Install production dependencies.
COPY ./requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Other env variables
ENV DEBUG $DEBUG
ENV HOST $HOST 
ENV PORT $PORT 
ENV SECRET $SECRET  
ENV BOT_TOKEN $BOT_TOKEN
ENV WEBHOOK_PATH $WEBHOOK_PATH  
ENV WEBHOOK_URL $WEBHOOK_URL 
ENV PAYMENTS_PROVIDER_TOKEN $PAYMENTS_PROVIDER_TOKEN
ENV ADMIN $ADMIN 

# Copy local code to the container image.
COPY . ./

# Expose container's port
EXPOSE $PORT

# Run the web service on container startup. Here we use the gunicorn
# webserver, with one worker process and 8 threads.
# For environments with multiple CPU cores, increase the number of workers
# to be equal to the cores available.
# Timeout is set to 0 to disable the timeouts of the workers to allow Cloud Run to handle instance scaling.
CMD exec gunicorn --bind 0.0.0.0:$PORT --workers 1 --worker-class uvicorn.workers.UvicornWorker --threads 8 --timeout 0 src.app:app
