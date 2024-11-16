import requests
from django.conf import settings
from some_module import get_mpesa_token, generate_password, generate_timestamp

def initiate_mpesa_payment(phone_number, amount):
    url = "https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest"
    headers = {
        "Authorization": f"Bearer {get_mpesa_token()}",
        "Content-Type": "application/json",
    }
    payload = {
        "BusinessShortCode": "174379",
        "Password": generate_password(),
        "Timestamp": generate_timestamp(),
        "TransactionType": "CustomerPayBillOnline",
        "Amount": amount,
        "PartyA": phone_number,
        "PartyB": "174379",
        "PhoneNumber": phone_number,
        "CallBackURL": "https://yourdomain.com/payment/callback/",
        "AccountReference": "Order12345",
        "TransactionDesc": "Payment for Order12345",
    }
    response = requests.post(url, json=payload, headers=headers)
    return response.json()
