from pprint import pprint
from django.conf import settings
from core.utils.model_choices import CurrencyChoices, PricingTypeChoices
import requests

HEADERS = {
    "X-CC-Api-Key": settings.COINBASE_API_KEY,
    "accept": "application/json",
    "content-type": "application/json",
    "X-CC-Version": "2018-03-22"
}



def create_charge(full_name:str, description):
    print(HEADERS)
    # data = {
    #     "name": "The Human Fund",
    #     "description": "Money For People",
    #     "pricing_type": "no_price"
    # }
    data = {
        "name": "Augusto Carrillo",
        "description": "Pago de Prueba",
        "pricing_type": PricingTypeChoices.FIXED_PRICE,
        "local_price": {
            "amount": 10,
            "currency": CurrencyChoices.USD
        },
        "metadata": {
            "product_order_id": 10,
            "store_id": 5
        },
        "redirect_url": "https://charge/completed/page",
        "cancel_url": "https://charge/canceled/page"
    }
    response = requests.post("https://api.commerce.coinbase.com/charges/", headers=HEADERS, json=data)
    pprint(response.json())

def get_charge(transaction_id:str):
    response = requests.get(f"https://api.commerce.coinbase.com/charges/{transaction_id}", headers=HEADERS)
    pprint(response.json(),indent=2)
