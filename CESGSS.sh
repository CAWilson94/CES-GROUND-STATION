#!/bin/bash
if [[ "$1" = "all" ]]; then
	echo "hello all"
	gnome-terminal -e "python manage.py runserver"
	gnome-terminal -e "celery -A cesGroundStation worker -l info"
	cd frontend/client && node server.js 
fi

if [[ "$1" = "" ]]; then
	echo Argument %1 not defined.
	echo 
	echo Choose one of the following:
	echo
	echo    1. all     - Start Django, Celery, and node
	echo         1.1 all site - Start all of the above and also open the webpage
	echo    2. django  - Start Django server
	echo    3. celery  - Start Celery server
	echo    4. node    - Start Node server
	echo    5. site    - Open the GSS webpage
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

if [[ "$1" = "site" ]]; then
	echo "hello site"
	sensible-browser "localhost:8081/"
fi

if [[ "$2" = "site" ]]; then
	echo "hello site"
	sensible-browser "localhost:8081/"
fi

