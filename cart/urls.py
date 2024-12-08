from django.urls import path
from . import views

urlpatterns = [
    path('', views.cart, name='cart'),  # Default cart view
    path('add/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('checkout/', views.checkout, name='checkout'),  # Checkout view
]
