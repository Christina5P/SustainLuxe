from django.urls import reverse
from django.contrib.auth import authenticate, login
from .models import UserProfile, User, Account
from .forms import UserProfileForm, SellerForm, WithdrawalForm
from checkout.models import Order
from .models import Product as ProfilesProduct
from products.models import Product as ProductsProduct
import uuid
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from decimal import Decimal
from django.db import transaction
from django.utils import timezone
from .utils import get_total_balance


@login_required
def profile(request):
    profile, created = UserProfile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully')
        else:
            messages.error(request, 'Update failed. Please ensure the form is valid.')
    else:
        form = UserProfileForm(instance=profile)

    template = 'profiles/profile.html'
    context = {
        'form': form,
        'on_profile_page': True
    }

    return render(request, template, context)


def sale_product(request):
    """Form for selling product
    """
    template = 'profiles/sale_product.html'

    if request.method == 'POST':
        form = SellerForm(request.POST)
        if form.is_valid():
            product = form.save(commit=False)
            product.sku = str(uuid.uuid4())
            product.user = request.user
            product.save()

            profile = request.user.userprofile
            profile.update_balance(product.price)

            request.session['save_info'] = {
                'sku': product.sku,
                'price': float(form.cleaned_data['price']),
            }
            messages.success(
                request, 'Your product has been listed successfully!'
            )
            return redirect('saleorder_success') 
    else:
        form = SellerForm()

    return render(request, template, {'form': form})


def saleorder_success(request,):
    """
    Handle successful Sale Registration
    """
    save_info = request.session.get('save_info')

    # Context to use for success confirmation
    if save_info:

        sku = save_info.get('sku', None)  
        price = save_info.get('price', None)  

        del request.session['save_info']

        return render(
            request,
            'profiles/saleorder_success.html',
            {'sku': sku, 'price': price},
        )
    else:
        messages.warning(request, 'No sale information confirmed.')
        form = SellerForm()

    return redirect('sale_product')


@login_required
def account_details(request, user_id):
    user = get_object_or_404(User, id=user_id)
    profile = user.userprofile
    account = get_object_or_404(Account, user=request.user)
    orders = Order.objects.filter(user_profile=profile)
    template = 'profiles/account_details.html'

    products = ProductsProduct.objects.filter(user=user, sold=False)
    sold_products = ProductsProduct.objects.filter(user=user, sold=True)

    # Använd den nya metoden för att beräkna tillgänglig balans
    available_balance = account.calculate_balance()
    withdrawal_history = account.withdrawal_history

    context = {
        'products': products,
        'sold_products': sold_products,
        'account': account,
        'available_balance': available_balance,
        'orders': orders,
        'user': request.user,
        'withdrawal_history': withdrawal_history,
    }

    return render(request, template, context)


@transaction.atomic
def withdrawal_view(request):
    account = get_object_or_404(Account, user=request.user)
    available_balance = account.calculate_balance()

    form = WithdrawalForm(
        account=account
    )  

    if request.method == 'POST':
        form = WithdrawalForm(request.POST, account=account)
        if form.is_valid():
            amount = form.cleaned_data['amount']
            if account.request_payout(amount):
                messages.success(request, 'Withdrawal requested successfully.')
            else:
                messages.error(request, 'Error processing withdrawal.')
            return redirect('withdrawal')

    form = WithdrawalForm(account=account)

    withdrawal_history = account.withdrawal_history
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
