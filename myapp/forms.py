from django import forms
from .models import Contact, Member, Product

class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ['name', 'email', 'subject', 'message']

class MemberForm(forms.ModelForm):
    class Meta:
        model = Member
        fields = '__all__'

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'description', 'price', 'stock', 'image']

        # Optional: Add widgets for custom styling (e.g., Bootstrap classes)
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter product name'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Enter product description'}),
            'price': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter price in KES'}),
            'stock': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter stock quantity'}),
            'image': forms.FileInput(attrs={'class': 'form-control'}),
        }