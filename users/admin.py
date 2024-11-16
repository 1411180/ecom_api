from django.contrib import admin
from .models import Cart, CartItem, Product, Message, Review, Receipt, Wishlist, FollowProduct, Payment

admin.site.register(Cart)
admin.site.register(CartItem)
admin.site.register(Product)
admin.site.register(Message)
admin.site.register(Review)
admin.site.register(Receipt)
admin.site.register(Wishlist)
admin.site.register(FollowProduct)
admin.site.register(Payment)
