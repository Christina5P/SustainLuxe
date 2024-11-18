from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import UserProfile
from .models import Sale


@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    """Create or update user profile"""
    if created:
        UserProfile.objects.create(user=instance)

    instance.userprofile.save()


@receiver(post_save, sender=User)
def create_sale_for_new_user(sender, instance, created, **kwargs):
    if created:
        Sale.objects.create(user=instance)
