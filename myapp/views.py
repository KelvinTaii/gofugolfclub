from django.shortcuts import render, redirect, get_object_or_404
from .forms import ContactForm, MemberForm, ProductForm
from django.contrib import messages
from .models import Member, Product, Cart
from django.contrib.auth.decorators import login_required

# Create your views here.
def index(request):
    return render(request,'index.html')
def about(request):
    return render(request,'about.html')

def services(request):
    return render(request,'services.html')
def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            # Save form data to the database
            form.save()
            messages.success(request, 'Your message has been sent successfully!')
            return redirect('contact')  # Redirect to the contact page (or any other page you choose)
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = ContactForm()

    return render(request, 'contact.html', {'form': form})

def membership(request):
    if request.method == 'POST':
        form = MemberForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('members_list')
    else:
        form = MemberForm()
    return render(request, 'membership.html', {'form': form})

def members_list(request):
    members = Member.objects.all()
    return render(request, 'members_list.html', {'members': members})

def shop(request):
    products = Product.objects.all()
    return render(request, 'shop.html', {'products': products})

def cart(request):
    cart_items = Cart.objects.all()
    total = sum(item.product.price * item.quantity for item in cart_items)
    return render(request, 'cart.html', {'cart_items': cart_items, 'total': total})


def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart_item, created = Cart.objects.get_or_create(product=product)
    if not created:
        cart_item.quantity += 1
    cart_item.save()
    return redirect('shop')


@login_required
def checkout(request):
    # Mpesa payment logic goes here
    return render(request, 'checkout.html')

def add_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()  # Save the product to the database
            return redirect('shop')  # Redirect to the home page or any success page
    else:
        form = ProductForm()

    return render(request, 'add-product.html', {'form': form})