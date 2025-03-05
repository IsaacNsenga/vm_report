from django.apps import AppConfig

class AppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'APP'

    def ready(self):
        import APP.signals  # Importer les signaux pour qu'ils soient pris en compte
