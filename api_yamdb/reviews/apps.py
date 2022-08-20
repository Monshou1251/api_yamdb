from django.apps import AppConfig


class ReviewsConfig(AppConfig):
    name = 'reviews'

    def ready(self):
        from . import signals
        signals.Review.connect(signals.update_rating)
