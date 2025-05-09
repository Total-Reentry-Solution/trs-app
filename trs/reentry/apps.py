from django.apps import AppConfig


class ReentryConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "reentry"

    def ready(self):
        import reentry.signals
