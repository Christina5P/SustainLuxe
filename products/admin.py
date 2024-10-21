from django.contrib import admin
from .models import Product, Category
from .models import Brand, Condition, Fabric, Size, Color 


# Register your models here.
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'sku',
        'brand',
        'size',
        'fabric',
        'price',
        'condition',
        'get_user'
    )
    list_filter = (
        'brand',
        'fabric',
        'size',
        'condition',
        'sku',
        'created_at',
        )
     

    list_filter = ('is_listed', 'sold')
    actions = ['list_products']

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


admin.site.register(Product, ProductAdmin)
admin.site.register(Category)
admin.site.register(Size)
admin.site.register(Brand)
admin.site.register(Condition)
admin.site.register(Fabric)
admin.site.register(Color)
