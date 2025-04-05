#!/bin/sh
set -e
export FLASK_APP=app

# Use pipenv if it's managing dependencies, fallback to system Python
if [ -f Pipfile ] && command -v pipenv > /dev/null && pipenv --venv > /dev/null 2>&1; then
  echo " * Running with Pipenv"
  pipenv run python init_db.py
  pipenv run flask --debug run -h 0.0.0.0 -p 3000
else
  echo " * Running with system Python"
  python init_db.py
  flask --debug run -h 0.0.0.0 -p 3000
fi