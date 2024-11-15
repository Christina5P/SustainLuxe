from django.urls import path
from . import views


urlpatterns = [
    path('', views.profile, name='profile'),
    path('sale_product/', views.sale_product, name='sale_product'),
    path(
        'saleorder_success/',
        views.saleorder_success,
        name='saleorder_success',
    ),
    path('order_history/', views.order_list, name='order_list'),
    path(
        'order_history/<str:order_number>/',
        views.order_history,
        name='order_history',
    ),
    path('withdrawal/', views.withdrawal_view, name='withdrawal'),
    path(
        'account/<int:user_id>/', views.account_details, name='account_details'
    ),
    
]
