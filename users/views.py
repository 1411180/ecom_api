import stripe
from django.shortcuts import render, redirect, get_object_or_404
from .models import Cart, CartItem, Product, Message, Review, Receipt, Wishlist, FollowProduct
from django.http import JsonResponse
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from .utils import initiate_mpesa_payment

stripe.api_key = settings.STRIPE_SECRET_KEY

def add_to_cart(request, product_id):
    product = Product.objects.get(id=product_id)
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
    cart_item.quantity += 1
    cart_item.save()
    return redirect('cart_detail')

def remove_from_cart(request, cart_item_id):
    cart_item = CartItem.objects.get(id=cart_item_id)
    cart_item.delete()
    return redirect('cart_detail')

def update_cart(request, cart_item_id, quantity):
    cart_item = CartItem.objects.get(id=cart_item_id)
    cart_item.quantity = quantity
    cart_item.save()
    return redirect('cart_detail')

def inbox(request):
    messages = Message.objects.filter(user=request.user).order_by('-created_at')
    message_data = [{
        'subject': message.subject,
        'content': message.content,
        'created_at': message.created_at,
    } for message in messages]

    return JsonResponse({'messages': message_data})

def add_review(request, product_id):
    product = Product.objects.get(id=product_id)
    if request.method == "POST":
        rating = request.POST.get('rating')
        comment = request.POST.get('comment')
        Review.objects.create(user=request.user, product=product, rating=rating, comment=comment)
    return redirect('product_detail', product_id=product.id)

def generate_receipt(request, order_id):
    order = Order.objects.get(id=order_id)
    receipt = Receipt.objects.create(
        user=request.user,
        total_amount=order.total_amount,
        transaction_id=order.transaction_id
    )
    receipt.products.set(order.products.all())
    return render(request, 'receipt.html', {'receipt': receipt})

def add_to_wishlist(request, product_id):
    product = Product.objects.get(id=product_id)
    wishlist, created = Wishlist.objects.get_or_create(user=request.user)
    wishlist.products.add(product)
    return redirect('wishlist')

def remove_from_wishlist(request, product_id):
    product = Product.objects.get(id=product_id)
    wishlist = Wishlist.objects.get(user=request.user)
    wishlist.products.remove(product)
    return redirect('wishlist')

def follow_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    FollowProduct.objects.get_or_create(user=request.user, product=product)
    return redirect('product_detail', product_id=product.id)

def unfollow_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    follow = get_object_or_404(FollowProduct, user=request.user, product=product)
    follow.delete()
    return redirect('product_detail', product_id=product.id)

def dashboard(request):
    cart_items = CartItem.objects.filter(cart__user=request.user)
    reviews = Review.objects.filter(user=request.user)
    receipts = Receipt.objects.filter(user=request.user)
    wishlist = Wishlist.objects.filter(user=request.user)
    return render(request, 'dashboard.html', {
        'cart_items': cart_items,
        'reviews': reviews,
        'receipts': receipts,
        'wishlist': wishlist
    })

def process_stripe_payment(request):
    if request.method == 'POST':
        try:
            data = request.POST
            charge = stripe.Charge.create(
                amount=int(data['amount']) * 100,
                currency="usd",
                source=data['stripeToken'],
                description="Payment for Order12345",
            )
            return JsonResponse({'status': 'success', 'charge': charge})
        except stripe.error.StripeError as e:
            return JsonResponse({'status': 'error', 'message': str(e)})

class MpesaPaymentAPIView(APIView):
    def post(self, request):
        phone_number = request.data.get('phone_number')
        amount = request.data.get('amount')
        response = initiate_mpesa_payment(phone_number, amount)
        return Response(response)

class StripePaymentAPIView(APIView):
    def post(self, request):
        return process_stripe_payment(request)

def mpesa_callback(request):
    return JsonResponse({'message': 'Mpesa callback received'})

def stripe_webhook(request):
    return JsonResponse({'message': 'Stripe webhook received'})
