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
    account, created = Account.objects.get_or_create(user_id=user_id)
    orders = Order.objects.filter(user_profile=profile)
    template = 'profiles/account_details.html'

    products = ProductsProduct.objects.filter(user=user, sold=False)
    sold_products = ProductsProduct.objects.filter(user=user, sold=True)

    total_revenue = get_total_balance(request.user)  # Använd funktionen här

    context = {
        'products': products,
        'sold_products': sold_products,
        'account': account,
        'total_revenue': total_revenue,
        'orders': orders,
        'user': user,
    }

    return render(request, template, context)

@login_required
def withdrawal_view(request):
    account = get_object_or_404(Account, user=request.user)

    # Använd get_total_balance för att hämta total revenue
    total_revenue = get_total_balance(request.user)

    if request.method == 'POST':
        amount = Decimal(request.POST.get('amount', 0))

        # Kontrollera att användaren har tillräckligt med pengar
        if amount <= total_revenue:
            # Logik för uttag
            account.withdrawal(amount)
            messages.success(request, 'Withdrawal successful.')
        else:
            messages.error(request, 'Insufficient funds for withdrawal.')

        return redirect('withdrawal')

    context = {
        'total_revenue': total_revenue,  # Skicka total_revenue till mallen
        'account': account,
    }

    return render(request, 'profiles/withdrawal.html', context)


@login_required
def order_list(request):
    orders = Order.objects.filter(user_profile=request.user.userprofile)
    return render(request, 'profiles/order_list.html', {'orders': orders})


@login_required
def order_history(request, order_number):
    order = get_object_or_404(
        Order, order_number=order_number, user_profile=request.user.userprofile
    )
    return render(request, 'checkout/checkout_success.html', {'order': order})
