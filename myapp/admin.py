from django.contrib import admin
from .models import Contact, Product, Member

@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'message', 'id', 'sent_at') # Customize fields to display in the admin
    ordering = ('-sent_at',)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'stock', 'created_at', 'updated_at')
    search_fields = ('name',)
    list_filter = ('created_at',)

@admin.register(Member)
class MemberAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'email', 'membership_type', 'joined_date')