from django.apps import AppConfig


class AuthenticationConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'authentication'

    """
    The below method is going to be called once during the app initialization
    process because the current class is called automatically by Django during
    the application initialization process
    """
    def ready(self):
        """
        Import the signals.This import statement will triggers the execution
        of the code defined in signals.py
        """
        from . import signals
