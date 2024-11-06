from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import UserProfile
from products .models import Product


@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    """
    Create or update the user profile
    """
    if created:
        UserProfile.objects.create(user=instance)
    # Existing users: just save the profile
    instance.userprofile.save()

    @receiver(post_save, sender=User)
    def create_or_update_sale_profile(sender, instance, created, **kwargs):
        if created:
            Sale.objects.create(user=instance)
        else:
            instance.sale.save()
