from django.contrib import admin
from .models import Order, OrderLineItem


# OrderLineItem inline-admin (för att visa orderrader på ordersidan)
class OrderLineItemAdminInline(admin.TabularInline):
    model = OrderLineItem
    readonly_fields = ('lineitem_total',)
    extra = 0


# Registrera Order-modellen
@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    inlines = (OrderLineItemAdminInline,)
    readonly_fields = (
        'order_number',
        'date',
        'order_total',
        'delivery_cost',
        'grand_total',
        'original_bag',
        'stripe_pid',
    )

    fields = (
        'order_number',
        'user_profile',
        'full_name',
        'email',
        'phone_number',
        'street_address1',
        'postcode',
        'town_or_city',
        'country',
        'date',
        'order_total',
        'delivery_cost',
        'grand_total',
        'original_bag',
        'stripe_pid',
    )

    list_display = (
        'order_number',
        'full_name',
        'date',
        'grand_total',
        'get_user_profile',
    )
    search_fields = ('order_number', 'full_name', 'email')
    list_filter = ('date',)

    def get_user_profile(self, obj):
        return obj.user_profile

    get_user_profile.short_description = 'User Profile'


# Registrera OrderLineItem-modellen separat
@admin.register(OrderLineItem)
class OrderLineItemAdmin(admin.ModelAdmin):
    list_display = (
        'order',
        'product',
        'quantity',
        'lineitem_total',
        'get_user_profile',
    )
    search_fields = ('order__order_number', 'product__name')

    def get_user_profile(self, obj):
        return obj.order.user_profile

    get_user_profile.short_description = 'User Profile'
