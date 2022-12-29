from pprint import pprint
from typing import Dict
from django.conf import settings
from core.models.order import Order
from core.utils.model_choices import CurrencyChoices, PricingTypeChoices
from django.urls import reverse
import requests

HEADERS = {
    "X-CC-Api-Key": settings.COINBASE_API_KEY,
    "accept": "application/json",
    "content-type": "application/json",
    "X-CC-Version": "2018-03-22"
}



def create_charge(full_name:str, description:str, amount:float, product_id:int) -> Dict:
    order = Order.objects.get(id=product_id)
    data = {
        "name": full_name,
        "description": description,
        "pricing_type": PricingTypeChoices.FIXED_PRICE,
        "local_price": {
            "amount": amount,
            "currency": CurrencyChoices.USD
        },
        "metadata": {
            "order_id": str(order.id),
        },
        "redirect_url": settings.BASE_URL+reverse(settings.COINBASE_SUCCESS_URL_NAME),
        "cancel_url": settings.BASE_URL+reverse(settings.COINBASE_CANCELLED_URL_NAME),
        # "cancel_url": f"{settings.BASE_URL}canceled/page"
        # "cancel_url": f"{settings.BASE_URL}canceled/page"
    }
    response = requests.post("https://api.commerce.coinbase.com/charges/", headers=HEADERS, json=data)
    if not response.status_code in [200,201]:
        raise ValueError(f"Error en Coinbase {response.text}")
    return response.json()

def get_charge(transaction_id:str):
    response = requests.get(f"https://api.commerce.coinbase.com/charges/{transaction_id}", headers=HEADERS)
    pprint(response.json(),indent=2)

def get_charges():
    response = requests.get(f"https://api.commerce.coinbase.com/charges/", headers=HEADERS)
    pprint(response.json(), indent=2)