from django.contrib import admin
from .models import Product, Category
from .models import Brand, Condition, Fabric, Size, Color


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'friendly_name')
    search_fields = ('name', 'friendly_name')


class ProductAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'sku',
        'price',
        'condition',
        'get_user',
        'sold',
        'return_option',
        'expired',
        'weight_in_kg',
    )
    list_filter = (
        'brand',
        'condition',
        'sku',
        'created_at',
        'sold',
        'return_option',
        'listed_at',
        'weight_in_kg',
    )
    actions = ['list_products', 'mark_for_return']
    search_fields = ('name', 'user__user__username')

    def list_products(self, request, queryset):
        for product in queryset:
            if not product.listed_at:
                product.list_product()
        self.message_user(
            request, f"{queryset.count()} product(s) have been listed."
        )

    list_products.short_description = "List selected products"

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
