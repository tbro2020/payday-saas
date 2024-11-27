from django.apps import AppConfig


class SanctionConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'sanction'

    def ready(self) -> None:
        import sanction.signals
