from typing import Dict, List
import uuid
from django.conf import settings
import base64
import requests
from core.models.order import Order

from core.serializers.paypal_serializers import PaypalItemsSerializer


PAYPAL_TOKEN = settings.PAYPAL_SECRET
CLIENT_ID = settings.PAYPAL_CLIENT_ID
BASE_URL = settings.PAYPAL_API


def generate_access_token():
    response = requests.post(f"{BASE_URL}/v1/oauth2/token", auth=(CLIENT_ID,PAYPAL_TOKEN),data="grant_type=client_credentials")
    return response.json().get("access_token")

def create_order(items : List[Dict], order: Order):
    token = generate_access_token()
    headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {token}"
    }
    order_first_item = {"amount":{"currency_code":"USD", "value":order.total_order, "reference_id":str(order.id)}}
    # serializer = PaypalItemsSerializer(data=items, many=True)
    # serializer.is_valid(raise_exception=True)
    # items = dict(serializer.data)
    print(items)
    url = f"{BASE_URL}/v2/checkout/orders"
    data = {
      "intent": "CAPTURE",
      "purchase_units": [
        order_first_item,
      ],
      "items":[
        *items
      ]
      
    }
    response = requests.post(url, headers=headers, json=data)
    return response.json()

def capture_order(order_id:str):
    token = generate_access_token()
    headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {token}"
    }
    url = f"{BASE_URL}/v2/checkout/orders/{order_id}/capture"
    response = requests.post(url, headers=headers)
    return response.json()