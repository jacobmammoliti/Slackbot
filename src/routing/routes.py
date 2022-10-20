"""This module is responsible for setting up a Flask instance
along with all the necessary routes.

This is only used when running in HTTP mode as Socket mode
does not require Flask.
"""
from flask import Flask, request
from slack_bolt.adapter.flask import SlackRequestHandler

def initialize_flask(app, request_handler_path):
    """Initializes a Flask application and sets up the routes.

    Args:
        app (Class): A class that provides functionalities to register middleware/listeners.
        request_handler_path (string): Path for Slack to send events to.

    Returns:
        flask_app (Class): Class of the Flask application
    """
    # Initialize Flask app
    flask_app = Flask(__name__)
    handler = SlackRequestHandler(app)

    # Create a Flask route to handle POST requests from Slack
    @flask_app.route(request_handler_path, methods=["POST"])
    def slack_events():
        """Sets up a Request URL path for Slack interactivity.

        Args:
            None

        Returns:
            Request handler for Slack bot.
        """
        return handler.handle(request)

    # Create a Flask route to handle health checks
    @flask_app.route("/healthz", methods=["GET"])
    def healthz():
        """Sets up a health check endpoint.

        Args:
            None

        Returns:
            A 200 HTTP healthy response code.
        """
        return "Healthy", 200

    return flask_app
