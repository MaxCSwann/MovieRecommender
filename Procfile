release: ./manage.py shell < populate-db.py
web: gunicorn movies.wsgi:application --log-file -