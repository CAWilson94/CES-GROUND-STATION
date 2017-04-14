@echo off

TITLE CESGSS

if "%1" equ "" goto :usage

if %1 equ all goto :all

if %1 equ django goto :django

if %1 equ celery goto :celery

if %1 equ node goto :node

if %1 equ site goto :site

if %1 equ colin goto :colin

if %1 equ clydespace goto :clydespace

if %1 equ ces goto :ces

:usage
echo Argument %1 not defined.
echo.
echo Choose one of the following:
echo.
echo    1. all     - Start Django, Celery, and node
echo         1.1 all site - Start all of the above and also open the webpage
echo    2. django  - Start Django server
echo    3. celery  - Start Celery server
echo    4. node    - Start Node server
echo    5. site    - Open the GSS webpage
goto:eof

:all
start cmd /c "celery -A cesGroundStation purge -f && celery -A cesGroundStation worker -l info"
start cmd /c "cd frontend/client && node server"
start cmd /c "python manage.py runserver"
if "%2" neq "site" goto :eof
if %2 equ site start "CES-Ground-Station" "http://localhost:8081"

goto :eof

:django
if "%2" equ "-c" (
	python manage.py runserver 
	goto :eof
)
start cmd /c "python manage.py runserver"
goto :eof

:celery
if "%2" equ "-c" (
	celery -A cesGroundStation purge -f
	celery -A cesGroundStation worker -l info
	goto :eof
)
start cmd /c "celery -A cesGroundStation purge -f && celery -A cesGroundStation worker -l info"
goto :eof

:node
if "%2" equ "-c" (
	cd frontend/client
	node server
	goto :eof
)
start cmd /c "cd frontend/client && node server"
goto :eof

:site
start "CES-Ground-Station" "http://localhost:8081"
goto :eof

:colin
echo Pray for Colin!
goto :eof

:clydespace
echo """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
echo "     ._______    .__.        __.     ___.  .     ._      ._______.  "
echo "     /  ___  \.     |        \      /  /   |  .__  \     |          "
echo "    /  /   \.       |         \.  ./ ./    |     \  \    |  |'      "
echo "   |  |             |          \     /     |      |  |   |  |___.   "
echo "  '| '|             |'          \  ./      |      '  |'  '  .___|   "
echo "   |  |     .       |          '|          '         |      |       "
echo "    \  \___/        |.    .     |                   /       |____.  "
echo "     \.          .________|    .|          _______./     ._______|  "
echo "                                                                    "
echo "     ._______     ._____.         ___.         _.        ._______.  "
echo "     /       \.   |  .__         / .          /  ___     |          "
echo "    /             |     \  .    /  \         /  /   \.   |  |'      "
echo "    \    .__      |     '  |   /    \  .    |  |         |  |___.   "
echo "     \__.   \    .|   .___/   /  .___\. \  '| '|         '  .___|   "
echo "   .         \    |      '   |  .______. |  |  |     .      |       "
echo "    \        /    |          |         | |   \  \___/       |____.  "
echo "     \______/    .|         .|         |_|    \_.        ._______|  "
echo ",,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,"
goto :eof

:ces
echo """"""""""""""""""""""""""""""""""""""""""""
echo "     ._______    ._______.    ._______    "
echo "     /  ___  \.  |            /       \.  "
echo "    /  /   \.    |  |'       /            "
echo "   |  |          |  |___.    \    .__     "
echo "  '| '|             .___|     \__.   \    "
echo "   |  |     .       |       .         \   "
echo "    \  \___/        |____.   \        /   "
echo "     \.          ._______|    \______/    "
echo "                                          "
echo "     ._______    ._______     ._______    "
echo "     /  ___  \.  /       \.   /       \.  "
echo "    /  /   \.   /            /            "
echo "   |  |   .     \    .__      \    .__    "
echo "   |  |'  |_  .  \__.   \      \__.   \   "
echo "   |  |     | | .        \   .         \  "
echo "   '   \___/ /   \        /   \        /  "
echo "        .___/     \______/     \______/   "
echo ",,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,"
goto :eof