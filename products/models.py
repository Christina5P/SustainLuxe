from django.db import models
from django.utils import timezone
from profiles.models import UserProfile
from django_countries.fields import CountryField

# Create your models here.


class Product(models.Model):
    name = models.CharField(max_length=254)
    sku = models.CharField(max_length=100, unique=True,)
    size = models.ForeignKey(
        'Size', on_delete=models.CASCADE
    )  
    image_url = models.URLField(null=True, blank=True)
    image = models.ImageField(null=True, blank=True)
    price = models.DecimalField(max_digits=6, decimal_places=2)
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
    user_profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True) 
    updated_at = models.DateTimeField(auto_now=True) 
    return_unsold = models.BooleanField(default=False)
    charge_for_unsold = models.BooleanField(default=False)
    sold = models.BooleanField(default=False) 
    sold_at = models.DateTimeField(null=True, blank=True)  

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
