"""This module holds all the functions to interact with HashiCorp Vault
including authentication and secret retrieval.

It is structured to abstract the initialization and retrieval of secrets
from the initialization module.
"""
import os
import sys
import logging
from hvac import Client
from hvac.api.auth_methods import Kubernetes
from hvac.exceptions import InvalidPath, Forbidden

def initialize_client():
    """Initializes a client connection to HashiCorp Vault.

    Args:
        None.

    Returns:
        client (class): The Client class for HashiCorp Vault.
    """
    logging.info("Connecting to HashiCorp Vault at %s", os.environ["VAULT_ADDR"])

    client = Client(url=os.environ["VAULT_ADDR"])

    # Call on the appropriate authentication method
    # based on the VAULT_AUTH_METHOD env var
    match os.environ["VAULT_AUTH_METHOD"]:
        case "kubernetes":
            kubernetes_auth_method(client)

    try:
        assert client.is_authenticated()
    except AssertionError as error:
        logging.error("Unable to authenticate to HashiCorp Vault. Got: %s", error)
        sys.exit(1)

    logging.info("Successfully authenticated to HashiCorp Vault.")

    return client

def retrieve_slack_secrets(client):
    """Retrieves the required Slack details from a KVv2
    path.

    Args:
        client (class): The Client class for HashiCorp Vault.

    Returns:
        credentials (dictionary): A dictionary of strings containing Slack credentials.
    """
    credentials = {}

    # Check if a specific mount point was set, if not
    # assume we start at 'secret/'
    mount_point = os.environ.get("VAULT_KV2_MOUNT_POINT", "secret")

    try:
        result = client.secrets.kv.v2.read_secret_version(
            mount_point=os.environ["VAULT_KV2_MOUNT_POINT"],
            path=os.environ["VAULT_SECRET_PATH"]
        )
    except InvalidPath as error:
        logging.error("Path not found: %s", error)

    try:
        credentials['slack_channel_id'] = result['data']['data']['slack_channel_id']
        credentials['slack_bot_token'] = result['data']['data']['slack_channel_id']

        if os.environ.get("SOCKET_MODE", False):
            credentials['slack_app_token'] = result['data']['data']['slack_app_token']
        else:
            credentials['slack_signing_secret'] = result['data']['data']['slack_signing_secret']
    except KeyError as error:
        logging.error("%s key not found at %s", error,
            mount_point + "/" + os.environ["VAULT_SECRET_PATH"])
        sys.exit(1)

    return credentials

def kubernetes_auth_method(client):
    """Authenticates to HashiCorp Vault via the Kubernetes
    authentication method.

    Args:
        client (class): The Client class for HashiCorp Vault.

    Returns:
        None.
    """
    token_file = open("/var/run/secrets/kubernetes.io/serviceaccount/token", encoding="utf8").read()

    logging.info("Authenticating to HashiCorp Vault with Kubernetes role: %s", os.environ.get("VAULT_KUBERNETES_ROLE", "default"))
    
    try:        
        Kubernetes(client.adapter).login(
            role=os.environ.get("VAULT_KUBERNETES_ROLE", "default"),
            mount_point = os.environ.get("VAULT_AUTH_MOUNT", "kubernetes"),
            jwt=token_file
        )
    except Forbidden as error:
        logging.error(error)
        sys.exit(1)

    token_file.close()
