from django.shortcuts import render, redirect, get_object_or_404
from .forms import ContactForm, MemberForm, ProductForm
from django.contrib import messages
from .models import Member, Product, Cart, CartItem
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.models import User


# Helper function to get or create a cart
def get_cart(request):
    if request.user.is_authenticated:
        cart = Cart.objects.filter(user=request.user).first()  # Get the first cart for authenticated users
        if not cart:
            cart = Cart.objects.create(user=request.user)  # Create a new cart if none exists
    else:
        session_key = request.session.session_key
        if not session_key:
            request.session.create()  # Create session if it doesn't exist
        cart = Cart.objects.filter(session_key=request.session.session_key).first()
        if not cart:
            cart = Cart.objects.create(session_key=request.session.session_key)  # Create a new cart if none exists
    return cart


# Home Page
def index(request):
    return render(request, 'index.html', {'page_title': 'Welcome to Gofu-Golf Club'})


# User Registration
def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        email = request.POST['email']

        # Validate user input
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists. Please choose another.')
            return redirect('register')
        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email already exists. Please use another.')
            return redirect('register')

        user = User.objects.create_user(username=username, password=password, email=email)
        messages.success(request, 'Registration successful! You can now log in.')
        return redirect('login')
    return render(request, 'register.html', {'page_title': 'Gofu-Golf | Sign Up'})


# User Login
def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth_login(request, user)
            messages.success(request, 'You are now logged in.')
            return redirect('index')
        else:
            messages.error(request, 'Invalid credentials, please try again.')
    return render(request, 'login.html', {'page_title': 'Gofu-Golf | Sign In'})


# User Logout
def logout(request):
    auth_logout(request)
    messages.success(request, 'You have been logged out.')
    return redirect('login')


# About Page
def about(request):
    return render(request, 'about.html', {'page_title': 'Gofu-Golf | About Us'})


# Services Page
def services(request):
    return render(request, 'services.html', {'page_title': 'Gofu-Golf | Our Services'})


# Contact Page
def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your message has been sent successfully!')
            return redirect('contact')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = ContactForm()

    return render(request, 'contact.html', {'page_title': 'Gofu-Golf | Contact Us', 'form': form})


# Membership Page
def membership(request):
    if request.method == 'POST':
        form = MemberForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Membership registration successful!')
            return redirect('members_list')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = MemberForm()
    return render(request, 'membership.html', {
        'form': form,
        'page_title': 'Gofu-Golf | Membership Registration'
    })


# Members List
def members_list(request):
    members = Member.objects.all()
    return render(request, 'members_list.html', {
        'members': members,
        'page_title': 'Gofu-Golf | Members List'
    })


# Shop Page
def shop(request):
    products = Product.objects.all()
    cart = get_cart(request)
    cart_item_count = cart.items.count()  # Get count of items in the cart
    return render(request, 'shop.html', {
        'products': products,
        'cart_item_count': cart_item_count,
        'page_title': 'Gofu-Golf | Shop With Us',
    })


# Cart Page
def cart(request):
    cart = get_cart(request)
    cart_items = cart.items.all()
    total_price = cart.total_price()  # Reuse total_price method from the Cart model
    return render(request, 'cart.html', {
        'cart_items': cart_items,
        'total_price': total_price,
        'page_title': 'Gofu-Golf | Your Cart',
    })


# Add to Cart
@login_required  # Ensure only logged-in users can access this view
def add_to_cart(request, product_id):
    # Check if the user is staff or authenticated
    if not request.user.is_authenticated or not (request.user.is_staff or request.user.is_authenticated):
        messages.error(request, "You need to be logged in to add items to the cart.")
        return redirect('login')

    product = get_object_or_404(Product, id=product_id)
    cart = get_cart(request)

    # Get or create a CartItem for the product in the user's cart
    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
    if not created:
        if product.stock >= cart_item.quantity + 1:
            cart_item.quantity += 1  # Increment quantity if product already in cart
            cart_item.save()
        else:
            messages.error(request, f"Insufficient stock for {product.name}.")
            return redirect('shop')
    else:
        if product.stock < 1:
            messages.error(request, f"{product.name} is out of stock.")
            return redirect('shop')
        cart_item.save()

    messages.success(request, f"{product.name} added to your cart!")
    return redirect('shop')

# Checkout Page
@login_required
def checkout(request):
    cart = get_cart(request)
    cart_items = cart.items.all()

    if request.method == "POST":
        for item in cart_items:
            if f"increase_{item.id}" in request.POST and item.product.stock > item.quantity:
                item.quantity += 1
                item.save()
            elif f"decrease_{item.id}" in request.POST and item.quantity > 1:
                item.quantity -= 1
                item.save()
            elif f"delete_{item.id}" in request.POST:
                item.delete()
                messages.success(request, f"Removed {item.product.name} from your cart.")
                return redirect('checkout')

        if "confirm_checkout" in request.POST:
            for item in cart_items:
                product = item.product
                if product.stock >= item.quantity:
                    product.stock -= item.quantity
                    product.save()
                else:
                    messages.error(request, f"Insufficient stock for {product.name}.")
                    return redirect('checkout')
            cart_items.delete()
            messages.success(request, "Checkout successful! Thank you for your purchase.")
            return redirect('shop')

    total_price = sum(item.total_price() for item in cart_items)
    return render(request, 'checkout.html', {
        'cart_items': cart_items,
        'total_price': total_price,
        'page_title': 'Shop | Checkout',
    })


# Add Product (Admin Functionality)
@login_required
def add_product(request):
    if not request.user.is_staff:
        messages.error(request, "You do not have permission to add products.")
        return redirect('index')

    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Product added successfully!')
            return redirect('shop')
    else:
        form = ProductForm()

    return render(request, 'add-product.html', {
        'form': form,
        'page_title': 'Gofu-Golf | Add Product',
    })
