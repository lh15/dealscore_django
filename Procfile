web: gunicorn dealscore.wsgi
worker: celery -A dealscore worker -l info
worker: celery -A dealscore beat -l info