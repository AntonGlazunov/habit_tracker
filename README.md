# Курсовая работа DRF

команда для добаления суперпользователя:

python manage.py csu

команды для запуска проекта:

python manage.py runserver

для Windows:

celery -A config worker -l INFO -P eventlet

celery -A config beat -l INFO 

для других систем:

celery -A config worker -l INFO

celery -A config beat -l INFO

