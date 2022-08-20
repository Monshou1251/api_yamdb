from decimal import Decimal

from django.db.models import Avg
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from .models import Review


def calculate_title_rating(title):
    result = title.reviews.all().aggregate(
        rating=Avg('score')
    )
    rating_val = round(result['rating'], 2)
    title.rating_val = Decimal(rating_val)
    title.save()


@receiver(post_save, sender=Review)
def update_rating(sender, instance, **kwargs):
    calculate_title_rating(instance.title)
    print('SAVED')


@receiver(post_delete, sender=Review)
def delete_rating(sender, instance, **kwargs):
    calculate_title_rating(instance.title)
    print('DELETED')
