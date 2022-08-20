from decimal import Decimal

from django.db.models import Avg
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from .models import Review


@receiver([post_save, post_delete], sender=Review)
def update_rating(sender, instance, **kwargs):
    result = instance.reviews.all().aggregate(
        rating=Avg('score')
    )
    instance.rating_val = Decimal(round(result['rating'], 2))
    instance.save()
