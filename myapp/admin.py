from django.contrib import admin
from .models import Contact, Product

@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'message', 'id', 'sent_at') # Customize fields to display in the admin
    ordering = ('-sent_at',)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'stock', 'created_at', 'updated_at')
    search_fields = ('name',)
    list_filter = ('created_at',)