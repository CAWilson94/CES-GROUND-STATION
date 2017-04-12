#!/bin/bash
if [[ "$1" = "all" ]]; then
	echo "hello all"
	gnome-terminal -e "python manage.py runserver"
	gnome-terminal -e "celery -A cesGroundStation worker -l info"
	cd frontend/client && node server.js
fi

if [[ "$1" = "django" ]]; then
	echo "hello django"
	python manage.py runserver
fi

if [[ "$1" = "celery" ]]; then
	echo "hello celery"
	celery -A cesGroundStation worker -l info
fi

if [[ "$1" = "node" ]]; then
	echo "hello node"
	cd frontend/client && node server.js
fi
