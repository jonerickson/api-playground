#!/bin/sh
DB_URL=${1:-"file:./database.sqlite"}
export DATABASE_URL=$DB_URL
npm run deploy
exec npm start