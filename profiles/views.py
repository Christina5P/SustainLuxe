from django.shortcuts import render, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from .models import UserProfile
from .forms import SignupForm

# from .forms import UserProfileForm

from checkout.models import Order

# Create your views here.


def profile(request):
    """Display the user's profile."""
    profile = get_object_or_404(UserProfile, user=request.user)

    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully')
        else:
            messages.error(request, 'Update failed')
    else:
        form = UserProfileForm(instance=profile)
    orders = profile.orders.all()

    template = 'profiles/profile.html'
    context = {'form': form, 'orders': orders, 'on_profile_page': True}

    return render(request, template, context)


@login_required
def withdraw_view(request):
    if request.method == 'POST':
        amount = float(request.POST.get('amount', 0))
        user_profile = get_object_or_404(UserProfile, user=request.user)

        if user_profile.withdraw(amount):
            messages.success(request, 'Withdrawal sucessful.')
        else:
            messages.error(request, 'Insufficient funds for withdrawal.')

        template = 'withdraw.html'

    return render(
        request,
        template,
    )


def order_history(request, order_number):
    order = get_object_or_404(Order, order_number=order_number)
    template = 'checkout/checkout_success.html'
    context = {
        'order': order,
        'from_profile': True,
    }

    return render(request, template, context)
