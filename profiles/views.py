from django.shortcuts import render, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from .models import UserProfile  
from .forms import UserProfileForm  
from checkout.models import Order
from .models import Account  


@login_required
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
def account_detail(request, user_id):
    account = get_object_or_404(Account, user_id=user_id)
    template = 'profiles/details.html'
    context = {
        'products': account.products.all() if hasattr(account, 'products') else [],
        'account' : account,
    }

    return render(request, template, context)


@login_required
def withdraw_view(request):
    account = get_object_or_404(Account, user=request.user)

    if request.method == 'POST':
        amount = float(request.POST.get('amount', 0))

        if account.withdraw(amount):
            messages.success(request, 'Withdrawal successful.')
        else:
            messages.error(request, 'Insufficient funds for withdrawal.')

            return redirect('account_detail', user_id=request.user.id)

        template = 'withdraw.html'
    return render( request, template )


@login_required
def order_history_list(request):
    orders = get_object_or_404(Order.objects.filter(full_name=request.user))
    template = 'profiles/orderhistory.html'
    context = {
        'orders': orders,
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
