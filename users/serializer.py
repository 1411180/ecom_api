from rest_framework import serializers
from django.contrib.auth.models import User
from .models import (
    Product, Cart, CartItem, Message, Review,
    Receipt, Wishlist, Shop, FollowProduct, Payment
)

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'name', 'price', 'description']

class CartSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    class Meta:
        model = Cart
        fields = ['id', 'user', 'product', 'quantity']

class CartItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)
    class Meta:
        model = CartItem
        fields = ['id', 'cart', 'product', 'quantity']

class MessageSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    class Meta:
        model = Message
        fields = ['id', 'user', 'content', 'created_at', 'read']

class ReviewSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    product = ProductSerializer(read_only=True)
    average_rating = serializers.ReadOnlyField()

    class Meta:
        model = Review
        fields = ['id', 'user', 'product', 'rating', 'comment', 'average_rating']

class ReceiptSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    products = ProductSerializer(many=True, read_only=True)

    class Meta:
        model = Receipt
        fields = ['id', 'user', 'products', 'total_amount', 'transaction_id', 'created_at']

class WishlistSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    products = ProductSerializer(many=True, read_only=True)

    class Meta:
        model = Wishlist
        fields = ['id', 'user', 'products', 'saved_at']

class ShopSerializer(serializers.ModelSerializer):
    class Meta:
        model = Shop
        fields = ['id', 'name']

class FollowProductSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    product = ProductSerializer(read_only=True)

    class Meta:
        model = FollowProduct
        fields = ['id', 'user', 'product', 'followed_at']

class PaymentSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Payment
        fields = [
            'id', 'user', 'card_number', 'cardholder_name',
            'expiry_date', 'cvv', 'amount', 'payment_date'
        ]
        extra_kwargs = {
            'card_number': {'write_only': True},
            'cvv': {'write_only': True},
        }
