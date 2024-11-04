from django.urls import reverse
from django.contrib.auth import authenticate, login
from .models import UserProfile, User, Account
from .forms import UserProfileForm, SellerForm, WithdrawalForm
from checkout.models import Order
from .models import Sale
from products.models import Product as ProductsProduct
import uuid
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from decimal import Decimal
from django.db import transaction
from django.utils import timezone
from .utils import get_total_balance
from django.core.paginator import Paginator
import json


@login_required
def profile(request):
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


def sale_product(request):
    """Form for selling product
    """
    template = 'profiles/sale_product.html'
    sale, created = Sale.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        form = SellerForm(request.POST)
        if form.is_valid():
            product = form.save(commit=False)
            product.sku = str(uuid.uuid4())
            product.user = request.user
            product.save()

            earned_amount = product.price 
            sale.update_balance(earned_amount)

            request.session['save_info'] = {
                'sku': product.sku,
                'earned_amount': float(earned_amount * Decimal('0.7')),
            }
            messages.success(
                request, 'Your Form has been sended!'
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
    profile, created = UserProfile.objects.get_or_create(user=request.user)
    try:
        account = Account.objects.get(user=user)
    except Account.DoesNotExist:
        messages.warning(
            request, "Account not found. Please create an account first."
        )
        return redirect('profile.html')

    account = get_object_or_404(Account, user=request.user) 
    orders = Order.objects.filter(user_profile=profile)
    template = 'profiles/account_details.html'
    products = ProductsProduct.objects.filter(user=request.user).order_by(
        '-created_at'
    )
    sold_products = ProductsProduct.objects.filter(user=user, sold=True)
    available_balance = account.calculate_balance()
    withdrawal_history = account.withdrawal_history
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
                messages.success(request, 'Withdrawal requested successfully.')
            else:
                messages.error(request, 'Error processing withdrawal.')
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
