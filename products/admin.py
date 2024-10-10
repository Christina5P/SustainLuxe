from django.contrib import admin
from .models import Product, Category, Size, Brand, Condition, Fabric, Size, Color 


# Register your models here.
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'brand', 'size', 'fabric', 'condition')
    search_fields = ('name', 'brand__name', 'fabric__name')
    list_filter = ('brand', 'fabric', 'size', 'condition')

admin.site.register(Product, ProductAdmin)
admin.site.register(Category)
admin.site.register(Size)
admin.site.register(Brand)
admin.site.register(Condition)
admin.site.register(Fabric)
admin.site.register(Color)
