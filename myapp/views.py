from django.shortcuts import render, redirect, get_object_or_404
from .forms import ContactForm, MemberForm, ProductForm
from django.contrib import messages
from .models import Member, Product, Cart
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.models import User


# Create your views here.
def index(request):
    return render(request, 'index.html')


def register(request):
    if request.method == 'POST':
        # Handle registration logic
        username = request.POST['username']
        password = request.POST['password']
        email = request.POST['email']

        # You can use Django's User model to create a user
        user = User.objects.create_user(username=username, password=password, email=email)
        messages.success(request, 'Registration successful! You can now log in.')
        return redirect('login')
    return render(request, 'register.html')


def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        # Authenticate the user
        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth_login(request, user)
            messages.success(request, 'You are now logged in.')
            return redirect('index')  # Redirect to home or any page you prefer
        else:
            messages.error(request, 'Invalid credentials, please try again.')
    return render(request, 'login.html')


def logout(request):
    auth_logout(request)
    messages.success(request, 'You have been logged out.')
    return redirect('login')


def about(request):
    return render(request, 'about.html')


def services(request):
    return render(request, 'services.html')


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
    cart_item_count = Cart.objects.filter(user=request.user).count() if request.user.is_authenticated else 0
    return render(request, 'shop.html', {'products': products, 'cart_item_count': cart_item_count})


def cart(request):
    if request.user.is_authenticated:
        cart_items = Cart.objects.filter(user=request.user)
        total = sum(item.product.price * item.quantity for item in cart_items)
        return render(request, 'cart.html', {'cart_items': cart_items, 'total': total})
    else:
        messages.error(request, 'You need to be logged in to view your cart.')
        return redirect('login')


def add_to_cart(request, product_id):
    if request.user.is_authenticated:
        product = get_object_or_404(Product, id=product_id)
        cart_item, created = Cart.objects.get_or_create(product=product,
                                                        user=request.user)  # Ensure the cart is tied to the user
        if not created:
            cart_item.quantity += 1
        cart_item.save()
        messages.success(request, "Item added to cart successfully!")
        return redirect('shop')
    else:
        messages.error(request, 'You need to be logged in to add items to your cart.')
        return redirect('login')


@login_required
def checkout(request):
    # You can add more functionality here (e.g., payment processing)
    return render(request, 'checkout.html')


def add_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('shop')
    else:
        form = ProductForm()

    return render(request, 'add-product.html', {'form': form})


def shop_view(request):
    products = Product.objects.all()
    cart_items = Cart.objects.filter(user=request.user)
    cart_item_count = cart_items.count()
    return render(request, 'shop.html', {'products': products, 'cart_item_count': cart_item_count})
