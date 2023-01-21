from core.models.order import Order
from django.template.loader import render_to_string
from django.conf import settings
from weasyprint import HTML

def generate_receipt(order: Order):

    context = {
        "order": order,
        "base_url": settings.BASE_URL
    }
    html = render_to_string("receipt.html", context)
    # with open("prueba.html", "w") as f:
    #     f.write(html)
    byte_data = HTML(string=html, base_url=settings.BASE_URL).write_pdf()

    return byte_data


