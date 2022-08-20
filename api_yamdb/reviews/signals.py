from django.db.models import Avg
from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver

from .models import Review


@receiver([post_save, post_delete], sender=Review)
def update_rating(sender, instance, **kwargs):
    title = instance.title
    result = title.reviews.aggregate(
        rating=Avg('score')
    )
    rating = result['rating']
    print(rating)
    title.rating_val = round(rating, 2) if rating else None
    title.save()
