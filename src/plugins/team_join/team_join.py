"""This module is called upon when a new user joins. It is responsible
for grabbing the ID of the new user and then relaying that information
to the specified channel.
"""
import logging
import os

def team_join(event, say):
    """Notifies a specific Slack channel when a new user joins the workspace.

    Args:
        event: An alias for payload in an @app.event listener. Registers a new event listener.
        say: Utility function, which calls chat.postMessage API with the associated channel ID.

    Returns:
        None.
    """
    user_id = event["user"]["id"]

    # Craft the message, log it, and write in channel
    text = f"<@{user_id}> has joined the workspace. Please give them a warm welcome!"
    logging.info("%s", text)
    say(text=text, channel=os.environ["SLACK_CHANNEL_ID"])
