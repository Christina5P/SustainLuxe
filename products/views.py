from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.db.models.functions import Lower
from .models import Product, Category, Brand, Condition, Size
from .forms import ProductForm, ProductFilterForm


def all_products(request):
    """A view to show all products, including sorting, filtering, and search queries"""

    products = Product.objects.all()
    categories = Category.objects.all()
    brand = Brand.objects.all()
    conditions = Condition.objects.all()
    sizes = Size.objects.all()
    query = request.GET.get('q', '')  
    category_id = request.GET.get('category')
    brand_id = request.GET.get('brand')
    condition_id = request.GET.get('condition')
    size_id = request.GET.get('size')
    sort = request.GET.get('sort', 'name')
    direction = request.GET.get('direction', 'asc')
    form = ProductFilterForm(request.GET)

    if category_id:
        products = products.filter(category__id=category_id)

    if brand_id:
        products = products.filter(brand__id=brand_id)

    if condition_id:
        products = products.filter(condition__id=condition_id)

    if size_id:
        products = products.filter(size__id=size_id)

    # Search functionality
    search_query = request.GET.get('q')
    if search_query:
        products = products.filter(name__icontains=search_query)

    # Sorting functionality
    if sort == 'name':
        sortkey = 'lower_name'
        products = products.annotate(lower_name=Lower('name'))
    elif sort == 'category':
        sortkey = 'category__name'
    elif sort == 'price':
        sortkey = 'price'
    else:
        sortkey = 'id'

    if direction == 'desc':
        sortkey = f'-{sortkey}'

    products = products.order_by(sortkey)

    context = {
        'products': products,
        'categories': categories,
        'brand': brand,
        'conditions': conditions,
        'sizes': sizes,
        'search_term': query,
        'current_sorting': f'{sort}_{direction}',
        'selected_category': category_id,
        'selected_brand': brand_id,
        'selected_condition': condition_id,
        'selected_size': size_id,
    }

    return render(request, 'products/products.html', context)


def product_list(request):
    products = Product.objects.filter(is_listed=True, sold=False)

    context = {
        'products': products,
    }

    return render(request, 'products/products.html', context)


def product_detail(request, product_id):
  
    product = get_object_or_404(Product, pk=product_id)

    context = {
        'product': product,
        'size': product.size,
        'brand': product.brand,
        'condition': product.condition,
        'fabric': product.fabric,
        'color': product.color,
    }

    return render(request, 'products/product_detail.html', context)


@login_required
def add_product(request):
  
    if not request.user.is_superuser:
        messages.error(request, 'Sorry, only store owners can do that.')
        return redirect(reverse('home'))

    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save()
            messages.success(request, 'Successfully added product!')
            return redirect(reverse('product_detail', args=[product.id]))
        else:
            messages.error(
                request,
                'Failed to add product. Please ensure the form is valid.',
            )
    else:
        form = ProductForm()

    template = 'products/add_product.html'
    context = {
        'form': form,
    }

    return render(request, template, context)


@login_required
def edit_product(request, product_id):
    
    if not request.user.is_superuser:
        messages.error(request, 'Sorry, only store owners can do that.')
        return redirect(reverse('home'))

    product = get_object_or_404(Product, pk=product_id)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, 'Successfully updated product!')
            return redirect(reverse('product_detail', args=[product.id]))
        else:
            messages.error(
                request,
                'Failed to update product. Please ensure the form is valid.',
            )
    else:
        form = ProductForm(instance=product)
        messages.info(request, f'You are editing {product.name}')

    template = 'products/edit_product.html'
    context = {
        'form': form,
        'product': product,
    }

    return render(request, template, context)


@login_required
def delete_product(request, product_id):
    
    if not request.user.is_superuser:
        messages.error(request, 'Sorry, only store owners can do that.')
        return redirect(reverse('home'))

    product = get_object_or_404(Product, pk=product_id)
    product.delete()
    messages.success(request, 'Product deleted!')
    return redirect(reverse('products'))
