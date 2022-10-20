"""This is the main entrypoint to the Slack bot.

This bot runs in two types of modes, Socket Mode for testing purposes,
and HTTP endpoint mode for real-world deployments. Refer to the
README in the repository for more information on how to run it
and to see the available configuration settings.
"""
import os
import logging
from slack_bolt import App
from initialization import http_listener, slack_authenticate
from plugins.register import register_plugins
from routing.routes import initialize_flask

logging.basicConfig(level=logging.INFO)

# Dictionary of required Slack credentials
credentials = slack_authenticate()

if os.environ.get("SOCKET_MODE", False):
    from slack_bolt.adapter.socket_mode import SocketModeHandler
    app = App(token=credentials['slack_bot_token'])
else:
    listen_port, listen_addr, request_handler_path = http_listener()

    # Initialize app with Bot Token and Signing Secret
    app = App(
        token=credentials['slack_bot_token'],
        signing_secret=credentials['slack_signing_secret']
    )

    # Initialize Flask routes here
    flask_app = initialize_flask(app, request_handler_path)

# Register plugins to the Slack bot
register_plugins(app)

if __name__ == "__main__":
    # Running directly
    if os.environ.get("SOCKET_MODE", False):
        logging.info("Running in Socket Mode.")
        SocketModeHandler(app, credentials['slack_app_token']).start()
    else:
        logging.info("Running in HTTP mode.")
        flask_app.run(host=listen_addr, port=int(listen_port))
else:
    logging.info("Running in HTTP endpoint mode.")
    # Running with gunicorn
    gunicorn_logger = logging.getLogger('gunicorn.error')
    app.logger.handlers = gunicorn_logger.handlers
    app.logger.setLevel(gunicorn_logger.level)