"""This modules contains functions that set up the HTTP listener and
logic to retrieve credentials to authenticate to Slack.

Any environment variables required and wrapped in a try except block
to ensure that the necessary information is provided. If not,
fail early and provide a useful message on what is missing.
"""

import os
import sys
import logging
from vault.client import initialize_client, retrieve_slack_secrets

def http_listener():
    """Sets up the listening port, bind address, and request handler path. Only used in HTTP mode.

    Args:
        None.

    Returns:
        listen_port (int): Port to listen on.
        listen_addr (string): Address to bind to.
        request_handler_path (string): Path for Slack to send events to.
    """
    try:
        listen_port = os.environ.get("LISTEN_PORT", 5000)
        listen_addr = os.environ.get("LISTEN_ADDR", "0.0.0.0")
        request_handler_path = os.environ.get("REQUEST_HANDLER_PATH", "/slack/events")
    except KeyError as error:
        logging.error("%s not set... exiting", error)
        sys.exit(1)

    return listen_port, listen_addr, request_handler_path

def slack_authenticate():
    """Routing function to determine where to get Slack credentials from.
    Currently supports retrieving credentials from environment variable
    or HashiCorp Vault.

    Args:
        None.

    Returns:
        credentials (dictionary): A dictionary of strings containing Slack credentials.
    """
    if "VAULT_ADDR" in os.environ:
        return _get_credentials_from_hashicorp_vault()

    return _get_credentials_from_environment_variables()

def _get_credentials_from_environment_variables():
    """Retrieves the required Slack credentials from environment variables.

    Args:
        None.

    Returns:
        credentials (dictionary): A dictionary of strings containing Slack credentials.
    """
    credentials = {}
    try:
        credentials['slack_channel_id'] = os.environ["SLACK_CHANNEL_ID"]
        credentials['slack_bot_token'] = os.environ["SLACK_BOT_TOKEN"]

        if os.environ.get("SOCKET_MODE", False):
            credentials['slack_app_token'] = os.environ["SLACK_APP_TOKEN"]
        else:
            credentials['slack_signing_secret'] = os.environ["SLACK_SIGNING_SECRET"]

    except KeyError as error:
        logging.error("%s not set... exiting", error)
        sys.exit(1)

    return credentials

def _get_credentials_from_hashicorp_vault():
    """Retrieves the required Slack credentials from HashiCorp Vault.

    Args:
        None.

    Returns:
        credentials (dictionary): A dictionary of strings containing Slack credentials.
    """
    # Authenticate to Vault with desired authentication method
    client = initialize_client()

    # Retrieve Slack credentials from KVv2 store
    credentials = retrieve_slack_secrets(client)

    return credentials
