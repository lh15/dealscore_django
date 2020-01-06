web: gunicorn dealscore.wsgi
worker: celery -A dealscore worker --concurrency=1
beat: celery -A dealscore beat -S django