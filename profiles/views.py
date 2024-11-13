# from django.db import models
# from django.urls import reverse
from django.contrib.auth import login  # authenticate
from .models import UserProfile, User, Account, Sale
from .forms import UserProfileForm, SellerForm, WithdrawalForm
from checkout.models import Order
from products.models import Product
import uuid
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from decimal import Decimal
from django.db import transaction
# from django.utils import timezone
# from .utils import get_total_balance
from django.core.paginator import Paginator
import json


@login_required
def profile(request):
    """ Update users profile settings"""
    profile, created = UserProfile.objects.get_or_create(user=request.user)
    account, account_created = Account.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(
                request,
                (
                    'Profile updated successfully'
                    if not created
                    else 'Account created successfully'
                ),
            )
            return redirect('profile')
        else:
            messages.error(
                request, 'Update failed. Please ensure the form is valid.'
            )
    else:
        form = UserProfileForm(instance=profile)

    template = 'profiles/profile.html'
    context = {
        'form': form,
        'profile': profile,
        'created': created,
        'on_profile_page': True,
        'account_created': account_created,
    }

    return render(request, template, context)


@login_required
def sale_product(request):
    """Form for selling a product"""
    template = 'profiles/sale_product.html'

    sale, created_sale = Sale.objects.get_or_create(user=request.user)
    account, created_account = Account.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        form = SellerForm(request.POST)
        if form.is_valid():
            product = form.save(commit=False)
            product.sku = str(uuid.uuid4())
            product.user = request.user
            product.save()

            earned_amount = product.price
            sale.update_balance_and_revenue(earned_amount)
            account.update_total_revenue(earned_amount)

            request.session['save_info'] = {
                'sku': product.sku,
                'price': float(earned_amount),
                'earned_amount': float(earned_amount * Decimal('0.7'))
            }

            messages.success(
                request,
                f'Your product has been listed for sale! '
                f'Product SKU: {product.sku}. '
                f'Sale price: EUR {product.price}.'
            )

            return redirect('saleorder_success')
    else:
        form = SellerForm()

    return render(request, template, {'form': form})


@login_required
def saleorder_success(request):
    """
    Handle successful Sale Registration
    """
    save_info = request.session.get('save_info')

    if save_info:
        sku = save_info.get('sku')
        price = save_info.get('price')
        earned_amount = save_info.get('earned_amount')

        return render(
            request,
            'profiles/saleorder_success.html',
            {
                'sku': sku,
                'price': price,
                'earned_amount': earned_amount,
            }
        )
    else:
        messages.warning(request, 'No sale information confirmed.')
        return redirect('sale_product')


@login_required
def account_details(request, user_id):
    """Account views balance and products for sale"""
    user = get_object_or_404(User, id=user_id)
    profile, created = UserProfile.objects.get_or_create(user=request.user)
    account, account_created = Account.objects.get_or_create(user=request.user)
    orders = Order.objects.filter(user_profile=profile)
    products = Product.objects.filter(user=request.user).order_by('-created_at')
    sold_products = Product.objects.filter(user=user, sold=True)
    template = 'profiles/account_details.html'

    available_balance = account.calculate_balance()

    withdrawal_history = (
        json.loads(account.withdrawal_history)
        if isinstance(account.withdrawal_history, str)
        else account.withdrawal_history
    )

    paginator = Paginator(products, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'products': products,
        'sold_products': sold_products,
        'account': account,
        'available_balance': available_balance,
        'orders': orders,
        'user': request.user,
        'withdrawal_history': withdrawal_history,
        'page_obj': page_obj,
    }

    return render(request, template, context)


@transaction.atomic
def withdrawal_view(request):
    account = get_object_or_404(Account, user=request.user)
    available_balance = account.calculate_balance()

    form = WithdrawalForm(account=account)

    if request.method == 'POST':
        form = WithdrawalForm(request.POST, account=account)
        if form.is_valid():
            amount = form.cleaned_data['amount']
            account.bank_account_number = form.cleaned_data[
                'bank_account_number'
            ]
            account.save()

            if account.request_payout(amount):
                account.process_payout()

                new_balance = account.calculate_balance()
                messages.success(
                    request,
                    f'Your withdrawal have been sent'
                    f'New balance: EUR {new_balance:}.'
                )

            return redirect('withdrawal')

    withdrawal_history = (
        json.loads(account.withdrawal_history)
        if isinstance(account.withdrawal_history, str)
        else account.withdrawal_history
    )
    pending_requests = account.get_pending_requests()

    context = {
        'form': form,
        'available_balance': available_balance,
        'user': request.user,
        'withdrawal_history': withdrawal_history,
        'pending_requests': pending_requests,
    }

    return render(request, 'profiles/withdrawal.html', context)


def order_list(request):
    orders = Order.objects.filter(user_profile=request.user.userprofile)
    return render(request, 'profiles/order_list.html', {'orders': orders})


@login_required
def order_history(request, order_number):
    order = get_object_or_404(
        Order, order_number=order_number, user_profile=request.user.userprofile
    )
    return render(request, 'checkout/checkout_success.html', {'order': order})
