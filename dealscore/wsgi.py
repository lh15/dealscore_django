"""
WSGI config for djangox_project project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/2.1/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dealscore.settings')

application = get_wsgi_application()

from dealsengine.tasks import start_crawling_threads
start_crawling_threads()
