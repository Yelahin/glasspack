from glasspack.settings.base import *

DEBUG = True

STORAGE = {
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedStaticFilesStorage",
    }
}

ALLOWED_HOSTS = ["localhost", "127.0.0.1"]


CSRF_TRUSTED_ORIGINS = [
    "http://localhost:8000",
    "http://127.0.0.1:8000",
]

# Make django listen to frontend app requests
CORS_ALLOW_ALL_ORIGINS = True