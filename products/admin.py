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
    list_filter = ('brand', 'fabric', 'size', 'condition', 'sku')

    search_fields = ('name', 'user__user__username')

    def get_user(self, obj):
        return obj.user.username
    get_user.short_description = 'User'


admin.site.register(Product, ProductAdmin)
admin.site.register(Category)
admin.site.register(Size)
admin.site.register(Brand)
admin.site.register(Condition)
admin.site.register(Fabric)
admin.site.register(Color)
