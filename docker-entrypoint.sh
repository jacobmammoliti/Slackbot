#!/bin/sh
set -e

if [ "$SOCKET_MODE" = true ] ; then
  python app.py
else
  gunicorn --bind :$LISTEN_PORT --workers 1 app:flask_app
fi