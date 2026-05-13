#!/usr/bin/env bash
# build.sh — Render runs this automatically on every deploy
# Make sure this file has execute permissions: chmod +x build.sh

set -o errexit  # exit immediately if any command fails

pip install -r requirements.txt

python manage.py collectstatic --no-input  # copies static files to staticfiles/
python manage.py migrate                   # runs any pending migrations
