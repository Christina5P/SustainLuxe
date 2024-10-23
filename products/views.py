from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.db.models.functions import Lower
from .models import Product, Fabric, Category, Brand, Condition, Size
from .forms import ProductForm, ProductFilterForm

main_categories = Category.objects.filter(parent_category=None)


def all_products(request):
    products = Product.objects.filter(is_listed=True, sold=False)
    categories = Category.objects.filter(parent_category=None)
    brands = Brand.objects.all()
    conditions = Condition.objects.all()
    sizes = Size.objects.all()
    fabric = Fabric.objects.all()

    query = request.GET.get('q', '')
    category_id = request.GET.get('category')
    brand_id = request.GET.get('brand')
    condition_id = request.GET.get('condition')
    size_id = request.GET.get('size')
    sort = request.GET.get('sort', 'name')
    direction = request.GET.get('direction', 'asc')

    form = ProductFilterForm(request.GET)

    if form.is_valid():
        if form.cleaned_data.get('categories'):
            products = products.filter(
                categories__in=form.cleaned_data['categories']
            )
        if form.cleaned_data.get('brands'):
            products = products.filter(brand__in=form.cleaned_data['brands'])
        if form.cleaned_data.get('conditions'):
            products = products.filter(
                condition__in=form.cleaned_data['conditions']
            )
        if form.cleaned_data.get('sizes'):
            products = products.filter(size__in=form.cleaned_data['sizes'])

    # Search functionality
    if query:
        products = products.filter(
            Q(name__icontains=query)
            | Q(description__icontains=query)
            | Q(brand__name__icontains=query)
        )

    # list functionality
    if category_id:
        category = get_object_or_404(Category, id=category_id)
        if category.parent_category:
            products = products.filter(categories=category)
        else:
            products = products.filter(Q(categories=category) | Q(categories__parent_category=category))

    # Sorting functionality
    if sort == 'name':
        sortkey = 'lower_name'
        products = products.annotate(lower_name=Lower('name'))
    elif sort == 'price':
        sortkey = 'price'
    elif sort == 'category':
        sortkey = 'categories__name'
    else:
        sortkey = 'name'

    if direction == 'desc':
        sortkey = f'-{sortkey}'

    products = products.order_by(sortkey)
    main_categories = Category.objects.filter(parent_category=None)

    context = {
        'products': products,
        'main_categories': main_categories,
        'brands': brands,
        'conditions': conditions,
        'sizes': sizes,
        'search_term': query,
        'current_sorting': f'{sort}_{direction}',
        'selected_category': category_id,
        'selected_brand': brand_id,
        'selected_condition': condition_id,
        'selected_size': size_id,
        'form': form,
        #'categories': categories,
    }

    return render(request, 'products/products.html', context)


def product_detail(request, product_id):

    product = get_object_or_404(Product, pk=product_id)
    carbon_saving = calculate_carbon_saving(product)
    fabrics = Fabric.objects.all()

    context = {
        'product': product,
        'size': product.size,
        'brand': product.brand,
        'condition': product.condition,
        'fabrics': fabrics,
        'color': product.color,
        'carbon_saving': carbon_saving,
    }

    return render(request, 'products/product_detail.html', context)


# To calculate sustainable. Just add more fabrics if needed
CARBON_EMISSIONS = {
    'cotton': 15,  # kg CO2 per kg of cotton
    'polyester': 30,  # kg CO2 per kg of polyester
    'wool': 20,  # kg CO2 per kg of wool
}


def calculate_carbon_saving(product):
    """
    Calculate carbon emission of products fabric and weight
    """
    fabric_name = product.fabric.name if product.fabric else None
    carbon_per_kg = CARBON_EMISSIONS.get(fabric_name.lower(), 0)
    return (
        carbon_per_kg * float(product.weight_in_kg)
        if product.weight_in_kg
        else 0
    )


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
