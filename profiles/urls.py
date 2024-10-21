from django.urls import path
from . import views
from .views import (
    account_details,
    order_history_list,
    withdraw_view,
)


urlpatterns = [
    path('', views.profile, name='profile'),
    path('sale_product/', views.create_sale, name='sale_product'), 
    path(
        'profile/order_history/',
        views.order_history_list,
        name='order_history_list',
    ),
    path('withdraw/', views.withdraw_view, name='withdraw'),
    path(
        'account/<int:user_id>/', views.account_details, name='account_details'
    ),
]