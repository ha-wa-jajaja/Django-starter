from django.apps import AppConfig


class BugbytesConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "bugbytes"

    def ready(self):
        from . import signals
