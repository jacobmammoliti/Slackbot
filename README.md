[![Slackbot CI](https://github.com/jacobmammoliti/Slackbot/actions/workflows/main.yml/badge.svg?branch=main)](https://github.com/jacobmammoliti/Slackbot/actions/workflows/main.yml)
[![Docker Pulls](https://img.shields.io/docker/pulls/jacobmammoliti/slackbot)](https://hub.docker.com/repository/docker/jacobmammoliti/slackbot)
# Slackbot
A Python based Slackbot to announce events to a given a workspace.

Currently supports announcing when:
* A user joins the workspace
* A new channel is created

![](images/new_channel.png)

## Run
This application can be run in two modes: Regular mode (where the application recieves app payloads via Request URLs) or [Socket Mode](https://api.slack.com/apis/connections/socket) (where the appliactions recieves app payloads via web sockets).

### Running in Socket Mode
Socket Mode is only meant for development purposes. See the section [Development](#development) on how to build and run in this mode.

### Running in Regular Mode
Regular mode is meant for non-development purposes. A Dockerfile is provided to run this as a container. A Makefile is also provided to easily build and tag the image.

Below is an example on how to run the application directly with Docker.
> Note: Only required variables are passed in. Please review the [Configuration Parameters](#configuration-parameters) table for any additional variables you may need to pass.

```bash
docker run -it \
-e SLACK_BOT_TOKEN="" \
-e SLACK_SIGNING_SECRET="" \
-e SLACK_CHANNEL_ID="" \
-p 5000:5000 \
jacobmammoliti/slackbot
```

### Configuration Parameters
All configuration parameters are based via environment variables.

| Name | Type | Purpose | Default |
|---|---|---|---|
| LISTEN_ADDR | `string` | Address to listen on | `0.0.0.0` |
| LISTEN_PORT | `int` | Port to listen on | `5000` |
| SOCKET_MODE | `bool` | Run application in Socket Mode | `False` |
| SLACK_CHANNEL_ID | `string` | The Slack channel ID to send requests to | None. Required. |
| SLACK_BOT_TOKEN | `string` | Bot token for the Slack application | None. Required. |
| SLACK_SIGNING_SECRET | `string` | Signing secret for the Slack application | None. Required if not running in Socket mode |
| SLACK_APP_TOKEN | `string` | Application token for the Slack application | None. Required if running in Socket mode |
| REQUEST_HANDLER_PATH | `string` | Path to expose the application on for Request URL | `/slack/events/` |

## Development
If you plan to work on this project, you will need [Python](https://www.python.org/) installed on your machine. Python 3.6+ is required.

### Creating a Slack App

1. Go to [api.slack.com](https://api.slack.com/) and click **Create an app**.
2. Click **From Scratch** and give it a name and workspace. Click Create App.
3. Click **OAuth & Permissions**, scroll down to **Scopes**, and under **Bot Token Scopes** add the following scopes:
    - `channels:read`
    - `users:read`
    - `chat:write`
4. Click **Event Subscriptions** and toggle on **Enable Events**.
5. Under **Subscribe to bot events** click **Add Bot User Event** and add the following:
    - `channel_created`
    - `team_join`
6. Click on **Install App** and click on **Install to Workspace**. Copy the token. This is your Bot token.

To run in Socket mode:

7. Click **Socket Mode** and under **Connect using Socket Mode**, toggle **Enable Socket Mode**.
8. Give your token a name and ensure it has `connections:write` scope, click **Generate**, and copy the token. This is your Application token.

To run in Regular mode:

9. Click on **Basic Information** and retrieve the **Signing Secret**.

### Building Your Environment
Set up your Python environment.
```bash
python3 -m venv venv

source venv/bin/activate

pip install -r requirements.txt
```

Export required environment variables.
```bash
# Run the application in Socket Mode
export SOCKET_MODE=true

# Copy your bot (xoxb) token from the OAuth & Permissions page
export SLACK_BOT_TOKEN=<your-bot-token>

# Copy your app token (xapp) from App-Level Tokens, on the Basic Information page
export SLACK_APP_TOKEN=<your-app-token>

# Define the channel to post requests into
export SLACK_CHANNEL_ID=<your-channel-id>
```

Run the program.
```bash
python3 src/app.py
```

### Building the Container Image
```bash
make docker-build
```