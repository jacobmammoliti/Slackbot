import os
import sys
import logging
from slack_bolt import App

logging.basicConfig(level=logging.INFO)

# Try to set all required environment variables
try:
    SLACK_CHANNEL_ID = os.environ["SLACK_CHANNEL_ID"]
    SLACK_BOT_TOKEN = os.environ["SLACK_BOT_TOKEN"]
    LISTEN_PORT = os.environ.get("LISTEN_PORT", 5000)
    LISTEN_ADDR = os.environ.get("LISTEN_ADDR", "0.0.0.0")
    SOCKET_MODE = os.environ.get("SOCKET_MODE", False)
    REQUEST_HANDLER_PATH = os.environ.get("REQUEST_HANDLER_PATH", "/slack/events")
except KeyError as error:
    logging.error("%s not set... exiting", error)
    sys.exit(1)

if SOCKET_MODE:
    logging.info("Running in Socket Mode.")
    from slack_bolt.adapter.socket_mode import SocketModeHandler

    app = App(token=SLACK_BOT_TOKEN)
else:
    logging.info("Running in regular mode.")

    # Regular mode requires a Signing Secret
    try:
        SLACK_SIGNING_SECRET = os.environ["SLACK_SIGNING_SECRET"]
    except KeyError as error:
        logging.error("%s not set... exiting", error)
        sys.exit(1)

    from flask import Flask, request
    from slack_bolt.adapter.flask import SlackRequestHandler

    # Initalize app with Bot Token and Signing Secret
    app = App(token=SLACK_BOT_TOKEN, signing_secret=SLACK_SIGNING_SECRET)

    # Intialize Flask app
    flask_app = Flask(__name__)
    handler = SlackRequestHandler(app)

    # Create a Flask route to handle POST requests from Slack
    @flask_app.route(REQUEST_HANDLER_PATH, methods=["POST"])
    def slack_events():
        '''Sets up a Request URL path for Slack interactivity.'''
        return handler.handle(request)

# When a channel is created, send a message to the specified channel
# Required scope: 'channels:read'
@app.event("channel_created")
def channel_created(event, say):
    channel_id = event["channel"]["id"]
    creator_id = event["channel"]["creator"]

    # Craft the message, log it, and write in channel
    text = f"New channel <#{channel_id}> created by <@{creator_id}>. Join if you dare!"
    logging.info("%s", text)
    say(text=text, channel=SLACK_CHANNEL_ID)

# When a user joins the workspace, send a message to the specified channel
# Required scope: 'users:read'
@app.event("team_join")
def team_join(event, say):
    user_id = event["user"]

    # Craft the message, log it, and write in channel
    text = f"<@{user_id}> has joined the workspace. Please give them a warm welcome!"
    logging.info("%s", text)
    say(text=text, channel=SLACK_CHANNEL_ID)

if __name__ == "__main__":
    # Configure gunicorn logger
    gunicorn_logger = logging.getLogger('gunicorn.error')
    app.logger.handlers = gunicorn_logger.handlers
    app.logger.setLevel(gunicorn_logger.level)

    if SOCKET_MODE:
        try:
            SocketModeHandler(app, os.environ["SLACK_APP_TOKEN"]).start()
        except KeyError as error:
            logging.error("%s not set... exiting", error)
            sys.exit(1)
    else:
        flask_app.run(host=LISTEN_ADDR, port=int(LISTEN_PORT))
