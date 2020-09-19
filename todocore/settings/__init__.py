from todocore.settings.base import *
from django.core.exceptions import ImproperlyConfigured

environment = os.environ.get("TODO_CORE_OVERRIDE")

if environment is None:
    raise ImproperlyConfigured("TODO_CORE_OVERRIDE not set")
elif environment == "develop":
    from todocore.settings.develop import *
elif environment == "production":
    from todocore.settings.production import *
