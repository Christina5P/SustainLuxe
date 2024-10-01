from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django_countries.fields import CountryField


class UserProfile(models.Model):
    """
    A user profile model for maintaining default
    delivery information and order history, account and status
    """

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=50, null=False, blank=False)
    email = models.EmailField(max_length=254, null=False, blank=False)
    phone_number = models.CharField(max_length=25, null=False, blank=False)
    street_address = models.CharField(max_length=80, null=False, blank=False)
    postcode = models.CharField(max_length=20, null=False, blank=False)
    town_or_city = models.CharField(max_length=40, null=False, blank=False)
    country = CountryField(blank_label='Country', null=False, blank=False)
    total_revenue = models.DecimalField(max_digits=10, decimal_places=2,default=0.00)
    withdrawal_history = models.JSONField(default=list, blank=True)

    def withdraw(self, amount):
        if amount <= self.total_revenue:
            self.total_revenue -= amount
            self.withdrawal_history.append(
                {'amount': amount, 'date': timezone.now()}
            )
            self.save()
            return True
        return False

    def __str__(self):
        return self.user.username


@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    """
    Create or update the user profile
    """
    if created:
        UserProfile.objects.create(user=instance)
        # Existing users: just save the profile
    instance.userprofile.save()
