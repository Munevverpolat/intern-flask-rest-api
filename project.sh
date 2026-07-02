#!/bin/bash

echo "Intern Flask REST API Project"

case "$1" in

run)
    echo "Starting Flask application..."
    source venv/bin/activate
    python run.py
    ;;

migrate)
    echo "Running database migration..."
    source venv/bin/activate
    flask db migrate -m "auto migration"
    flask db upgrade
    ;;

logs)
    echo "Showing application logs..."
    tail -f logs/app.log
    ;;

*)
    echo "Usage:"
    echo "./project.sh run"
    echo "./project.sh migrate"
    echo "./project.sh logs"
    ;;

esac

