from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from myapp import views

urlpatterns = [
    path('admin/', admin.site.urls),

    # Authentication URLs
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('register/', views.register, name='register'),

    # Other Pages
    path('', views.index, name='index'),  # Home Page (you can update this as needed)
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),

    # Membership and Members list
    path('registration/', views.membership, name='membership'),
    path('members/', views.members_list, name='members_list'),

    # Shop and Cart URLs
    path('shop/', views.shop, name='shop'),
    path('cart/', include(('cart.urls', 'cart'), namespace='cart')),
    path('add-to-cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('add-product/', views.add_product, name='add_product'),

    # Services Page
    path('services/', views.services, name='services'),
]

# Serve media files during development
if settings.DEBUG:  # This ensures it only works in development mode
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
