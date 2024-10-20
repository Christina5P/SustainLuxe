from django.db import models
from django.utils import timezone
from datetime import timedelta
from django.contrib.auth.models import User
from django_countries.fields import CountryField
from django.core.validators import MinValueValidator, MaxValueValidator
from decimal import Decimal
from django.conf import settings

# Create your models here.


class Product(models.Model):
    name = models.CharField(max_length=254)
    sku = models.CharField(max_length=100, unique=True,)
    size = models.ForeignKey(
        'Size', on_delete=models.CASCADE
    )  
    image_url = models.URLField(null=True, blank=True)
    image = models.ImageField(null=True, blank=True)
    price = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.01'))],
    )
    brand = models.ForeignKey(
        'Brand', null=True, blank=True, on_delete=models.SET_NULL
    )  
    sustainable = models.TextField(max_length=25, null=True, blank=True)
    condition = models.ForeignKey(
        'Condition', on_delete=models.CASCADE
    )  
    fabric = models.ForeignKey('Fabric',
        max_length=254, null=True, blank=True, on_delete=models.SET_NULL
    )
    color = models.ForeignKey('Color',
        max_length=254, null=True, blank=True, on_delete=models.SET_NULL
    )
    category = models.ForeignKey(
        'Category',  
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )
    description = models.TextField(null=True, blank=True)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True
    )
    created_at = models.DateTimeField(auto_now_add=True) 
    updated_at = models.DateTimeField(auto_now=True) 
    return_option = models.BooleanField(
        default=False,
        verbose_name="Return unsold product?",
        help_text="Check this if you want to pay for return shipping. If unchecked, unsold items will be donated.")
    sold_at = models.DateTimeField(null=True, blank=True)  

    def time_until_expiration(self):
        if self.sold_at:
            return None 
        expiration_date = self.listed_at + timedelta(days=90)
        remaining_time = expiration_date - timezone.now()
        if remaining_time.total_seconds() <= 0:
            return None 
        return remaining_time

    def __str__(self):
        return self.name

# Lägg till intäkten till användarens saldo


def mark_as_sold(self):
    self.sold = True
    self.sold_at = timezone.now()
    self.user_profile.total_revenue += (
        self.price
    )  
    self.user_profile.save()
    self.save()


class Size(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Fabric(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Color(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Condition(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField(max_length=50, blank=True, null=True)

    def __str__(self):
        return self.name


class Category(models.Model):
    """
    Model for Categories with fields for category name, description,
    created, updated
    """
    name = models.CharField(max_length=60)
    friendly_name = models.CharField(max_length=100, null=True, blank=True)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "categories"

    def get_friendly_name(self):
        return self.friendly_name

    def __str__(self):
        return self.name


class Brand(models.Model):
    name = models.CharField(max_length=100, unique=True)  
    description = models.TextField(max_length=254, null=True, blank=True) 
    logo = models.ImageField(upload_to='brands/logos/', null=True, blank=True) 

    def __str__(self):
        return self.name
