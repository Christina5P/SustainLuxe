from django.shortcuts import (
    render,
    redirect,
    reverse,
    # HttpResponse,
    get_object_or_404,
)
from django.contrib import messages

from products.models import Product


def view_bag(request):
    """A view that renders the bag contents page"""

    return render(request, 'bag/bag.html')


def add_to_bag(request, item_id):
    """Add a quantity of the specified product to the shopping bag"""

    product = get_object_or_404(Product, pk=item_id)
    redirect_url = request.POST.get('redirect_url')
    size = request.POST.get('item_size') or 'N/A'
    quantity = int(request.POST.get('quantity', 1))
    bag = request.session.get('bag', {})

    if item_id not in bag:
        bag[item_id] = {'size': size, 'quantity': quantity}
        messages.success(request, f'Added {product.name} to your bag')
    else:
        messages.info(request, f'{product.name} is already in your bag')

    request.session['bag'] = bag
    return redirect(redirect_url)


def adjust_bag(request, item_id):
    """Adjust the quantity of the specified product to the specified amount"""

    product = get_object_or_404(Product, pk=item_id)
    size = request.POST.get('item_size')
    bag = request.session.get('bag', {})

    if item_id in bag:
        if size:
            bag[item_id]['size'] = size
            messages.success(request, f'Updated {product.name} size to {size}')

        else:
            messages.error(request, f'{product.name} is not in your bag')

    request.session['bag'] = bag
    return redirect(reverse('view_bag'))


def remove_from_bag(request, item_id):
    """Remove the item from the shopping bag"""

    product = get_object_or_404(Product, pk=item_id)
    bag = request.session.get('bag', {})

    if item_id in bag:
        del bag[item_id]
        messages.success(request, f'Removed {product.name} from your bag')
    else:
        messages.error(request, f'{product.name} is not in your bag')

    request.session['bag'] = bag
    return redirect('view_bag')
