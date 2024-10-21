from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.utils import timezone
from .models import OrderLineItem, Order 
from products.models import Product


@receiver(post_save, sender=OrderLineItem)
def update_on_save(sender, instance, created, **kwargs):
    """
    Update order total and product availability on lineitem update/create
    """
    try:
        instance.order.update_total()
        if created:
            product = instance.product
            product.mark_as_sold()
    except Exception as e:
        print(f"Error in update_on_save: {e}")


@receiver(post_delete, sender=OrderLineItem)
def update_on_delete(sender, instance, **kwargs):
    """
    Update order total on lineitem delete
    """
    try:
        instance.order.update_total()
    except Order.DoesNotExist:
        print(f"Order for OrderLineItem {instance.id} does not exist.")
    except Exception as e:
        print(f"Error in update_on_delete: {e}")


@receiver(post_save, sender=Order)
def update_product_sold_at(sender, instance, created, **kwargs):
    """
    Update product status when an order is created
    """
    if created:
        try:
            for line_item in instance.lineitems.all():
                product = line_item.product
                if hasattr(product, 'mark_as_sold'):
                    product.mark_as_sold()
                else:
                    product.sold = True
                    product.sold_at = timezone.now()
                    product.is_available = False
                    product.save()
        except Exception as e:
            print(f"Error in update_product_sold_at: {e}")
