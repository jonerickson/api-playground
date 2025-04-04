#!/bin/sh
DB_PATH=${1:-"../database.sqlite"}
export DATABASE_PATH=$DB_PATH
pipenv run flask --app "./books/index.py" --debug run -h 0.0.0.0 -p 3000