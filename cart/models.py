from django.db import models
from django.contrib.auth.models import User
from myapp.models import Product  # Assuming Product model is in the shop app


class Cart(models.Model):
    """
    Represents a cart, either for an authenticated user or a session-based user.
    """
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, null=True, blank=True, related_name="cart_set_1"  # Unique related_name
    )
    session_key = models.CharField(max_length=100, null=True, blank=True)  # For guest users
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Cart - {self.user or self.session_key}"


class CartItem(models.Model):
    """
    Represents an item in the cart.
    """
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def total_price(self):
        return self.product.price * self.quantity

    def __str__(self):
        return f"{self.quantity} x {self.product.name} in Cart {self.cart.id}"
