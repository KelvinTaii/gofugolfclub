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
        # For authenticated users, ensure only one cart exists
        cart = Cart.objects.filter(user=request.user).first()  # Get the first cart
        if not cart:
            cart = Cart.objects.create(user=request.user)  # Create a new cart if none exists
    else:
        # For guests, use session_key to get or create a cart
        session_key = request.session.session_key
        if not session_key:
            request.session.create()  # Create session if it doesn't exist
        cart = Cart.objects.filter(session_key=request.session.session_key).first()
        if not cart:
            cart = Cart.objects.create(session_key=request.session.session_key)  # Create a new cart if none exists
    return cart


# Home Page
def index(request):
    return render(request, 'index.html')


# User Registration
def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        email = request.POST['email']

        user = User.objects.create_user(username=username, password=password, email=email)
        messages.success(request, 'Registration successful! You can now log in.')
        return redirect('login')
    return render(request, 'register.html')


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
    return render(request, 'login.html')


# User Logout
def logout(request):
    auth_logout(request)
    messages.success(request, 'You have been logged out.')
    return redirect('login')


# About Page
def about(request):
    return render(request, 'about.html')


# Services Page
def services(request):
    return render(request, 'services.html')


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

    return render(request, 'contact.html', {'form': form})


# Membership Page
def membership(request):
    if request.method == 'POST':
        form = MemberForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('members_list')
    else:
        form = MemberForm()
    return render(request, 'membership.html', {'form': form})


# Members List
def members_list(request):
    members = Member.objects.all()
    return render(request, 'members_list.html', {'members': members})


# Shop Page
def shop(request):
    products = Product.objects.all()
    cart = get_cart(request)
    cart_item_count = cart.items.count()  # Get count of items in the cart
    return render(request, 'shop.html', {'products': products, 'cart_item_count': cart_item_count})


# Cart Page
def cart(request):
    cart = get_cart(request)
    cart_items = cart.items.all()
    total_price = cart.total_price()  # Reuse total_price method from the Cart model
    return render(request, 'cart.html', {'cart_items': cart_items, 'total_price': total_price})


# Add to Cart
def add_to_cart(request, product_id):
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
    cart = get_cart(request)  # Function to retrieve the user's cart
    cart_items = cart.items.all()

    if request.method == "POST":
        # Handle quantity update and delete actions
        for item in cart_items:
            # Increase Quantity
            if f"increase_{item.id}" in request.POST:
                if item.product.stock > item.quantity:  # Ensure stock is sufficient
                    item.quantity += 1
                    item.save()

            # Decrease Quantity
            elif f"decrease_{item.id}" in request.POST:
                if item.quantity > 1:  # Ensure quantity doesn't go below 1
                    item.quantity -= 1
                    item.save()

            # Delete Item
            elif f"delete_{item.id}" in request.POST:
                item.delete()
                messages.success(request, f"Removed {item.product.name} from your cart.")
                return redirect('checkout')

        # Handle checkout confirmation
        if "confirm_checkout" in request.POST:
            for item in cart_items:
                product = item.product
                if product.stock >= item.quantity:
                    product.stock -= item.quantity
                    product.save()
                else:
                    messages.error(request, f"Insufficient stock for {product.name}.")
                    return redirect('checkout')

            # Clear the cart after checkout
            cart_items.delete()
            messages.success(request, "Checkout successful! Thank you for your purchase.")
            return redirect('shop')

        # Handle cart update button
        messages.success(request, "Cart updated successfully!")
        return redirect('checkout')

    total_price = sum(item.total_price() for item in cart_items)
    return render(request, 'checkout.html', {'cart_items': cart_items, 'total_price': total_price})

# Add Product (Admin Functionality)
@login_required
def add_product(request):
    if not request.user.is_staff:
        # If the user is not an admin, redirect them or show an error message
        messages.error(request, "You do not have permission to add products.")
        return redirect('/')  # Redirect to a home or other page
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Product added successfully!')
            return redirect('shop')
    else:
        form = ProductForm()

    return render(request, 'add-product.html', {'form': form})
