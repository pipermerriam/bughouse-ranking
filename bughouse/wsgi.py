"""
WSGI config for bughouse-rankings project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/howto/deployment/wsgi/
"""
import os
import dotenv


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "bughouse.settings")

dotenv.load_dotenv(os.environ['ENV_CONFIGURATION_PATH'])


from django.core.wsgi import get_wsgi_application  # NOQA
application = get_wsgi_application()
