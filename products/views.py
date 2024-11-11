from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.db.models.functions import Lower
from .models import (
    Product,
    Category,
    Fabric,
    Brand,
    Condition,
    Size,
    ProductImage,
)
from .forms import ProductForm, ProductFilterForm
from decimal import Decimal, ROUND_DOWN
from django.core.paginator import Paginator
from django.db.models import Prefetch


def all_products(request):
    products = Product.objects.filter(is_listed=True, sold=False)
    main_categories = Category.objects.filter(
        parent_categories=None
    ).prefetch_related(
        Prefetch('subcategories', queryset=Category.objects.all())
    )

    form = ProductFilterForm(request.GET)

    brands = Brand.objects.all()
    conditions = Condition.objects.all()
    sizes = Size.objects.all()
    query = request.GET.get('q', '')
    category_id = request.GET.get('category')
    brand_id = request.GET.get('brand')
    condition_id = request.GET.get('condition')
    size_id = request.GET.get('size')
    sort = request.GET.get('sort', 'name')
    direction = request.GET.get('direction', 'asc')

    if form.is_valid():
        categories = form.cleaned_data.get('categories')
        brands = form.cleaned_data.get('brands')
        conditions = form.cleaned_data.get('conditions')
        sizes = form.cleaned_data.get('sizes')

        if categories:
            category_filters = Q()
            for category in categories:
                if category.parent_categories.exists():
                    descendant_ids = category.subcategories.all().values_list('id', flat=True)
                    category_filters |= Q(categories=category) | Q(categories__in=descendant_ids)
                else:
                    category_filters |= Q(categories=category)
            products = products.filter(category_filters).distinct()

        if brands:
            products = products.filter(brand__in=brands)
        if conditions:
            products = products.filter(condition__in=conditions)
        if sizes:
            products = products.filter(size__in=sizes)

    # Search functionality
    if query:
        products = products.filter(
            Q(name__icontains=query)
            | Q(description__icontains=query)
            | Q(brand__name__icontains=query)
        )

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
    main_categories = Category.objects.filter(parent_categories=None)
    paginator = Paginator(products, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

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
        'page_obj': page_obj,
    }

    return render(request, 'products/products.html', context)


def product_detail(request, product_id):

    product = get_object_or_404(Product, pk=product_id)
    carbon_saving = calculate_carbon_saving(product)
    fabrics = Fabric.objects.all()
    images = ProductImage.objects.filter(product=product)

    context = {
        'product': product,
        'size': product.size,
        'brand': product.brand,
        'condition': product.condition,
        'fabrics': fabrics,
        'color': product.color,
        'carbon_saving': carbon_saving,
        'images': images,
    }

    return render(request, 'products/product_detail.html', context)


def calculate_carbon_saving(product):
    """
    Calculate carbon emission of the given product's fabric and weight.
    """
    if product.fabric:
        carbon_per_kg = product.fabric.carbon_emission_per_kg  
        total_saving = carbon_per_kg * product.weight_in_kg
      
        total_saving = total_saving.quantize(Decimal('0.01'), rounding=ROUND_DOWN)
        return total_saving

    return Decimal(0).quantize(Decimal('0.01'), rounding=ROUND_DOWN)


@login_required
def product_emissions_view(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    total_emissions = calculate_carbon_saving(product)

    context = {
        'product': product,
        'total_emissions': total_emissions,
    }

    return render(request, 'product.html', context)


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
