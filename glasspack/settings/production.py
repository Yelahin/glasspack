from glasspack.settings.base import *

DEBUG = False

STORAGE = {
    "staticfiles": {}
}

ALLOWED_HOSTS = env("DJANGO_ALLOWED_HOSTS", default="*").split(" ")


CSRF_TRUSTED_ORIGINS = [
    # Put domain here
    "example.com"
]