web: gunicorn dealscore.wsgi
worker: celery -A dealscore worker
beat: celery -A dealscore beat -S django