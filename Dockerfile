FROM python:3.10.5-slim-bullseye

# Create non-root user
RUN useradd -m -d /home/worker worker

# Copy files to non-root user home directory
ENV APP_HOME /home/worker
WORKDIR $APP_HOME
COPY src/* requirements.txt docker-entrypoint.sh ./

# Install dependencies and fix permissions
RUN pip install -U pip && pip install -r requirements.txt && chown -R worker: $APP_HOME && chmod u+x docker-entrypoint.sh

# Switch to non-root user
USER worker

# Start application
ENTRYPOINT ["./docker-entrypoint.sh"]