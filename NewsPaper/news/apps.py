from django.apps import AppConfig


class NewsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'news'

    # override ready method to import all handler functions from signals
    def ready(self):
        import news.signals
