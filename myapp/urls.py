from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from myapp import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('registration/', views.membership, name='membership'),
    path('members/', views.members_list, name='members_list'),
    path('shop/', views.shop, name='shop'),
    path('cart/', views.cart, name='cart'),
    path('add-to-cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('add-product/', views.add_product, name='add_product'),
    path('services/', views.services, name='services'),
]

# Serve media files during development
if settings.DEBUG:  # This ensures it only works in development mode
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
