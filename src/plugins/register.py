import logging

from slack_bolt import App

from plugins.channel_created.channel_created import channel_created
from plugins.team_join.team_join import team_join

def register_plugins (app: App):
    """Registers plugins to the Slack bot.

    Args:
      app: A class that provides functionalities to register middleware/listeners.

    Returns:
        None.
    """

    plugin_list = [
        "channel_created", 
        "team_join"
    ]

    for plugin in plugin_list:
        app.event(plugin)(eval(plugin))
        logging.info("Successfully registered plugin: %s", plugin)