from django.urls import path
from . import views, MpesaPaymentAPIView, StripePaymentAPIView
from .views import login_view
from django.conf import settings
from django.conf.urls.sattic import static

urlpatterns = [
    path('add_to_cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('remove_from_cart/<int:cart_item_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('update_cart/<int:cart_item_id>/<int:quantity>/', views.update_cart, name='update_cart'),
    path('cart_detail/', views.cart_detail, name='cart_detail'),
    path('inbox/', views.inbox, name='inbox'),
    path('product/<int:product_id>/add_review/', views.add_review, name='add_review'),
    path('generate_receipt/<int:order_id>/', views.generate_receipt, name='generate_receipt'),
    path('wishlist/add/<int:product_id>/', views.add_to_wishlist, name='add_to_wishlist'),
    path('wishlist/remove/<int:product_id>/', views.remove_from_wishlist, name='remove_from_wishlist'),
    path('product/<int:product_id>/follow/', views.follow_product, name='follow_product'),
    path('product/<int:product_id>/unfollow/', views.unfollow_product, name='unfollow_product'),
    path('payment/mpesa/', MpesaPaymentAPIView.as_view(), name='mpesa-payment'),
    path('payment/stripe/', StripePaymentAPIView.as_view(), name='stripe-payment'),
    path('api/', include(router.urls)),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
