from django.apps import AppConfig


class UsersAppConfig(AppConfig):

    name = "wenhu.users"
    verbose_name = "Users"

    def ready(self):
        try:
            import wenhu.users.signals  # noqa F401
        except ImportError:
            pass
