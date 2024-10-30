from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='home'),
    path('sell/', views.sell_clothes, name='sell'),
    path('sustainable/', views.sustainable_view, name='sustainable'),
]
