import json
import stripe
from django.shortcuts import render, redirect, get_object_or_404
from .models import Cart, CartItem, Product, Message, Review, Receipt, Wishlist, FollowProduct
from django.http import JsonResponse
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from .forms import PaymentForm, ProductForm

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

def add_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('product_list')
    else:
        form = ProductForm()
    return render(request, 'add_product.html', {'form' : form})
    
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

@csrf_exempt
@login_required
def process_payment(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            amount = data.get("amount")
            token = data.get("token")

            if not amount or not token:
                return JsonResponse({"error": "Invalid input."}, status=400)

            amount_in_cents = int(float(amount) * 100)

            charge = stripe.Charge.create(
                amount=amount_in_cents,
                currency="usd",
                source=token,
                description=f"Payment by {request.user.username}",
            )

            payment = Payment.objects.create(
                user=request.user,
                amount=amount,
                stripe_charge_id=charge.id,
            )
            payment.save()

            return JsonResponse({"message": "Payment processed successfully."})

        except stripe.error.CardError as e:
            return JsonResponse({"error": f"Payment failed: {e.error.message}"}, status=400)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
    else:
        return JsonResponse({"error": "Invalid request method."}, status=405)
        
class ProductListView(APIView):
    def get(self, request):
        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)

class CartListView(APIView):
    def get(self, request):
        carts = Cart.objects.filter(user=request.user)
        serializer = CartSerializer(carts, many=True)
        return Response(serializer.data)

class CartItemListView(APIView):
    def get(self, request):
        cart_items = CartItem.objects.filter(cart__user=request.user)
        serializer = CartItemSerializer(cart_items, many=True)
        return Response(serializer.data)

class MessageListView(APIView):
    def get(self, request):
        messages = Message.objects.filter(user=request.user)
        serializer = MessageSerializer(messages, many=True)
        return Response(serializer.data)

class ReviewListView(APIView):
    def get(self, request):
        reviews = Review.objects.filter(user=request.user)
        serializer = ReviewSerializer(reviews, many=True)
        return Response(serializer.data)

class ReceiptListView(APIView):
    def get(self, request):
        receipts = Receipt.objects.filter(user=request.user)
        serializer = ReceiptSerializer(receipts, many=True)
        return Response(serializer.data)

class WishlistListView(APIView):
    def get(self, request):
        wishlist = Wishlist.objects.filter(user=request.user)
        serializer = WishlistSerializer(wishlist, many=True)
        return Response(serializer.data)

class FollowProductListView(APIView):
    def get(self, request):
        followed_products = FollowProduct.objects.filter(user=request.user)
        serializer = FollowProductSerializer(followed_products, many=True)
        return Response(serializer.data)

class PaymentListView(APIView):
    def get(self, request):
        payments = Payment.objects.filter(user=request.user)
        serializer = PaymentSerializer(payments, many=True)
        return Response(serializer.data)

@api_view(['POST'])
def make_payment(request):
    try:
        data = request.data
        amount = data.get('amount')
        currency = data.get('currency', 'usd')
        card_number = data.get('card_number')
        exp_month = data.get('exp_month')
        exp_year = data.get('exp_year')
        cvc = data.get('cvc')

        intent = stripe.PaymentIntent.create(
            amount=amount,
            currency=currency,
            payment_method_data={
                "type": "card",
                "card": {
                    "number": card_number,
                    "exp_month": exp_month,
                    "exp_year": exp_year,
                    "cvc": cvc,
                },
            },
            confirm=True,
        )

        return Response({"status": "success", "payment_intent": intent})

    except stripe.error.CardError as e:
        return Response({"status": "failure", "error": str(e)}, status=400)

        
        
