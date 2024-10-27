# utils.py

from decimal import Decimal
from .models import Account


def get_total_balance(user):
    try:
        account = Account.objects.get(user=user)
        return account.calculate_balance()
    except Account.DoesNotExist:
        return Decimal('0.00')
