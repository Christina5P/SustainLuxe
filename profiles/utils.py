from decimal import Decimal
from products.models import Product as ProductsProduct


def get_total_balance(user):
    """Beräkna total revenue för en användare baserat på sålda produkter."""
    sold_products = ProductsProduct.objects.filter(user=user, sold=True)
    total_revenue = sum(product.price for product in sold_products) * Decimal(
        '0.7'
    )  # 70% av försäljningspriset
    return total_revenue
