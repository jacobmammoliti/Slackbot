FROM python:3.10.8-slim-bullseye

# Define current version of the application.
ARG VERSION=0.1.0

# Create a non-root user.
RUN useradd -m -d /home/worker worker

# Copy files to non-root user home directory
ENV APP_HOME /home/worker
WORKDIR $APP_HOME
COPY src/* requirements.txt docker-entrypoint.sh ./

# Install dependencies 
RUN pip install -U pip && pip install -r requirements.txt && chown -R worker: $APP_HOME

# Switch to non-root user
USER worker

# 5000/tcp is the default interface that the application listens on.
EXPOSE 5000

# Start application
ENTRYPOINT ["./docker-entrypoint.sh"]