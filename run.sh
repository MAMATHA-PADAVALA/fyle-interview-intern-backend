#!/bin/bash

# to stop on first error
set -e

# Debug: Print current directory and list files
echo "Current directory: $(pwd)"
ls -la

# Delete older .pyc files
echo "Deleting old .pyc files..."
find . -type d \( -name env -o -name venv  \) -prune -false -o -name "*.pyc" -exec rm -rf {} \;

# Run required migrations (if any)
export FLASK_APP=core/server.py
echo "FLASK_APP is set to $FLASK_APP"

# Uncomment these lines if you need to run migrations
# echo "Initializing DB..."
# flask db init -d core/migrations/
# echo "Migrating DB..."
# flask db migrate -m "Initial migration." -d core/migrations/
# echo "Upgrading DB..."
# flask db upgrade -d core/migrations/

# Run server and log output
echo "Starting Gunicorn..."
gunicorn -c gunicorn_config.py core.server:app --log-level debug --access-logfile gunicorn-access.log --error-logfile gunicorn-error.log
