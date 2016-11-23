"""
WSGI config for social_football project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.8/howto/deployment/wsgi/
"""

import os, sys, django.core.handlers.wsgi

from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "social_football.settings")

application = django.core.handlers.wsgi.WSGIHandler()