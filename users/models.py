from django.db import models
from django.contrib.auth.models import User

class Product(models.Model):
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField(blank=True, null=True)

class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="Cart")
    product = models.ForeignKey("Product", on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

class Message(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    read = models.BooleanField(default=False)

class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    rating = models.PositiveIntegerField()
    comment = models.TextField()

    def average_rating(self):
        reviews = Review.objects.filter(product=self.product)
        return reviews.aggregate(models.Avg('rating'))['rating__avg']

class Receipt(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    products = models.ManyToManyField(Product)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    transaction_id = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

class Wishlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    products = models.ManyToManyField(Product)
    saved_at = models.DateTimeField(auto_now_add=True)

class Shop(models.Model):
    name = models.CharField(max_length=255)

class FollowProduct(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    followed_at = models.DateTimeField(auto_now_add=True)

class Payment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="payments")
    card_number = models.CharField(max_length=16)  # Mask this in production!
    cardholder_name = models.CharField(max_length=255)
    expiry_date = models.DateField()
    cvv = models.CharField(max_length=3)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Payment by {self.user.username} on {self.payment_date}"
