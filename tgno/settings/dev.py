from os import getenv as env

from .base import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "django-insecure-)u4^uo@zde4qa=m+*6x0$r$iro8k5&-=w$%)tf$vj(yf@wg#c="

# SECURITY WARNING: define the correct hosts in production!
ALLOWED_HOSTS = ["*"]

EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

WAGTAILADMIN_BASE_URL = "http://localhost:8000"

WAGTAILAPI_BASE_URL = "http://localhost:8000"


try:
    from .local import *
except ImportError:
    pass
