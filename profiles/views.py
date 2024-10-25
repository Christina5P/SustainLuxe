from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from .models import UserProfile, User, Account
from .forms import UserProfileForm, SellerForm
from checkout.models import Order
from products.models import Product
import uuid
from decimal import Decimal


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

    products = Product.objects.filter(user=user, sold=False)

    for product in products:
        remaining_time = product.time_until_expiration()
        if remaining_time:
            product.days_left = remaining_time.days
        else:
            product.days_left = None

    sold_products = Product.objects.filter(user=user, sold=True)
    total_revenue = sum(product.price for product in sold_products) * Decimal(
        '0.7'
    )

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

    if request.method == 'POST':
        amount = float(request.POST.get('amount', 0))

        if account.withdrawal(amount):
            messages.success(request, 'Withdrawal successful.')
        else:
            messages.error(request, 'Insufficient funds for withdrawal.')

            return redirect('account_details', user_id=request.user.id)

        template = 'withdrawal.html'
    return render(request, template)

@login_required
def order_list(request):
    orders = Order.objects.filter(user_profile=request.user.userprofile)
    return render(request, 'profiles/order_list.html', {'orders': orders})

@login_required
def order_history(request, order_number):
    order = get_object_or_404(Order, order_number=order_number, user_profile=request.user.userprofile)
    return render(request, 'checkout/checkout_success.html', {'order': order})

"""
@login_required
def order_list(request):
    profile = request.user.userprofile
    orders = profile.orders.all()
    template = 'profiles/order_history.html'
    context = {'orders': orders}
    return render(request, template, context)


def order_history(request, order_number):
    order = get_object_or_404(Order, order_number=order_number)

    messages.info(
        request,
        (
            f'This is a past confirmation for order number {order_number}. '
            'A confirmation email was sent on the order date.'
        ),
    )

    template = 'checkout/checkout_success.html'
    context = {
        'order': order,
        'from_profile': True,
    }

    return render(request, template, context)

    def create_account(request):
        if request.method == 'POST':
            form = CreateAccountForm(request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, 'Account created successfully!')
                return redirect(
                    'profile'
                )  
        else:
            form = CreateAccountForm()

        return render(request, 'profiles/create_account.html', {'form': form})
    """
