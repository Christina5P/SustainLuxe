from django.contrib import admin
from .models import Product, Category, ProductImage
from .models import Brand, Condition, Fabric, Size, Color
from django.utils import timezone


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'friendly_name')
    search_fields = ('name', 'friendly_name')


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 2


class ListedAtFilter(admin.SimpleListFilter):
    title = 'listed_at'
    parameter_name = 'listed'

    def lookups(self, request, model_admin):
        return (
            ('yes', 'Yes'),
            ('no', 'No'),
        )

    def queryset(self, request, queryset):
        if self.value() == 'yes':
            return queryset.filter(listed_at__isnull=False)
        elif self.value() == 'no':
            return queryset.filter(listed_at__isnull=True)
        return queryset

    def list_products(self, request, queryset):
        updated_count = 0
        for product in queryset:
            if not product.listed_at:
                product.listed_at = timezone.now()
                product.is_listed = True
                product.save()
                updated_count += 1
        self.message_user(
            request, f"{updated_count} product(s) have been listed."
        )

    list_products.short_description = "List selected products"

    def unlist_products(self, request, queryset):
        print("Unlisting selected products")
        """
        Clear the 'listed_at' field to unlist products.
        """
        updated_count = 0
        for product in queryset:
            if product.listed_at:
                product.listed_at = None
                product.is_listed = False
                product.save()
                updated_count += 1
        self.message_user(
            request, f"{updated_count} product(s) have been unlisted."
        )

    unlist_products.short_description = "Unlist selected products"

    def mark_for_return(self, request, queryset):
        updated_count = 0
        for product in queryset:
            if not product.return_option: 
                product.return_option = True
                product.save()
                updated_count += 1

    mark_for_return.short_description = "Mark selected products for return"


class ProductAdmin(admin.ModelAdmin):
    readonly_fields = ('sku',)

    list_display = (
        'get_user',
        'name',
        'created_at',
        'listed_at',
        'sold',
        'return_option',
        'expired',
        'sku',
        'price',
        'condition',
    )

    list_filter = (
        'created_at',
        'sold',
        'return_option',
        'listed_at',
        'sku',
        'brand',
        'condition',
        ListedAtFilter,
    )

    actions = ['list_products', 'mark_for_return']
    search_fields = ['name', 'user__username']
    inlines = [ProductImageInline]

    def get_user(self, obj):
        if obj.user:
            return obj.user.username
        return "No user"

    get_user.short_description = 'User'


admin.site.register(Category, CategoryAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Size)
admin.site.register(Brand)
admin.site.register(Condition)
admin.site.register(Fabric)
admin.site.register(Color)
