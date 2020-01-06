web: gunicorn dealscore.wsgi
main_worker: celery -A dealscore worker --beat --loglevel=info