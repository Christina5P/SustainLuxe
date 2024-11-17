from django.db import models
from django.utils import timezone
from datetime import timedelta, datetime
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from decimal import Decimal
from django.conf import settings
from django.utils.text import slugify
import uuid
from profiles.models import Sale


class Category(models.Model):
    """
    Model for Categories with fields for category name, description,
    created, updated
    """

    name = models.CharField(max_length=100)
    friendly_name = models.CharField(max_length=254, blank=True, null=True)
    parent_categories = models.ManyToManyField(
        'self', blank=True, related_name='subcategories', symmetrical=False
    )

    def get_friendly_name(self):
        return self.friendly_name if self.friendly_name else self.name

    def __str__(self):
        return self.name


class Meta:
    verbose_name_plural = 'Categories'


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
    weight_in_kg = models.DecimalField(
        max_digits=5, decimal_places=2, null=True, blank=True
    )
    categories = models.ManyToManyField(
        Category, related_name='products', blank=True
    )

    description = models.TextField(null=True, blank=True)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name='products',
    )
    created_at = models.DateTimeField(auto_now_add=True)
    listed_at = models.DateTimeField(null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_listed = models.BooleanField(default=False)
    return_option = models.BooleanField(
        default=False,
        verbose_name="Return unsold product?",
        help_text="Check this if you want to pay for return shipping. If unchecked, unsold items will be donated.")
    sold_at = models.DateTimeField(null=True, blank=True)
    sold = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.name} ({self.fabric.name} - {self.weight_in_kg} kg)"

    def save(self, *args, **kwargs):
        if not self.sku:
            self.sku = slugify(self.name) + "-" + str(uuid.uuid4())[:8]
        super().save(*args, **kwargs)

    def time_until_expiration(self):
        if self.sold_at:
            return None
        if self.listed_at:
            expiration_date = self.listed_at + timedelta(days=90)
            remaining_time = expiration_date - timezone.now()
        if remaining_time.total_seconds() <= 0:
            return None
        return remaining_time

    def expired(self):
        if self.listed_at and not self.sold:
            expiration_date = self.listed_at + timedelta(days=90)
            return timezone.now() > expiration_date
        return False

    def list_product(self):
        if not self.is_listed:
            self.is_listed = True
            self.listed_at = timezone.now()
            self.save()

    def mark_as_sold(self):
        if not self.sold:
            self.sold = True
            self.sold_at = timezone.now()
            self.is_listed = False
            self.save()

            try:
                sale = Sale.objects.get(user=self.user)
            except Sale.DoesNotExist:
                sale = Sale.objects.create(user=self.user)

            sale.update_balance_and_revenue(self.price)


class Size(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Fabric(models.Model):
    name = models.CharField(max_length=50)
    carbon_emission_per_kg = models.DecimalField(
        max_digits=10, decimal_places=2
    )

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


class Brand(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(max_length=254, null=True, blank=True)
    logo = models.ImageField(upload_to='media', null=True, blank=True)

    def __str__(self):
        return self.name


class ProductImage(models.Model):
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name='images'
    )
    image = models.ImageField(upload_to='media')


def __str__(self):
    return f"Image for {self.product.name}"
