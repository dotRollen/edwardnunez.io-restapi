#!/bin/bash
. /home/ubuntu/app-backend/env/bin/activate

NAME="web_backend"

echo "Starting $NAME as `whoami`"

while true; do
    flask deploy
    if [[ "$?" == "0" ]]; then
        break
    fi
    echo Deploy command failed, retrying in 5 secs...
    sleep 5
done

exec gunicorn -b :5000 --access-logfile - --error-logfile - backend.manage:app
