@echo off

TITLE CESGSS

if %1 equ all goto :all

if %1 equ django goto :django

if %1 equ celery goto :celery

if %1 equ node goto :node

if %1 equ site goto :site

:all
start cmd /c "celery -A cesGroundStation purge -f && celery -A cesGroundStation worker -l info"
start cmd /c "cd frontend/client && node server"
start cmd /c "python manage.py runserver"
goto :eof

:django
start cmd /c "python manage.py runserver"
goto :eof

:celery
start cmd /c "celery -A cesGroundStation purge -f && celery -A cesGroundStation worker -l info"
goto :eof

:node
start cmd /c "cd frontend/client && node server"
goto :eof

:site
start "CES-Ground-Station" "http://localhost:8081"
