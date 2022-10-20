"""This module is called upon when a new channel is created. It is
responsible for grabbing the ID of the new channel along with the
user that created it and then relaying that information to the
specified channel.
"""

import logging
import os

def channel_created(event, say):
    """Notifies a specific Slack channel when a new channel is created.

    Args:
      event: An alias for payload in an @app.event listener. Registers a new event listener.
      say: Utility function, which calls chat.postMessage API with the associated channel ID.

    Returns:
        None.
    """
    channel_id = event["channel"]["id"]
    creator_id = event["channel"]["creator"]

    # Craft the message, log it, and write in channel
    text = f"New channel <#{channel_id}> created by <@{creator_id}>. Join if you dare!"
    logging.info("%s", text)
    say(text=text, channel=os.environ["SLACK_CHANNEL_ID"])
