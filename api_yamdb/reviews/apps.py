from django.apps import AppConfig

from django.core.signals import request_finished


class ReviewsConfig(AppConfig):
    name = 'reviews'

    def ready(self):
        import reviews.signals
