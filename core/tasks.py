from celery import shared_task
from django.core.mail import EmailMessage
from core.controllers.receipt_controller import generate_receipt
from django.conf import settings
from django.template.loader import render_to_string
from django.core.files.uploadedfile import SimpleUploadedFile
from core.models.store import Store
from core.utils.image import generate_picture_to_django_user, generate_picture_to_store
from core.models.order import Order

@shared_task
def generate_profile_pic(user_email:str):
    generate_picture_to_django_user(user_email)
    return True
    
@shared_task
def generate_store_pic(store_id:int):
    store = Store.objects.get(id=store_id)
    generate_picture_to_store(store)
    return True

@shared_task
def send_receipt(order_id:int):
    order = Order.objects.get(id=order_id)
    receipt = generate_receipt(order)
    file = SimpleUploadedFile(f"orden-{order_id}",receipt, content_type="application/pdf")
    order.receipt = file
    order.save()
    html = render_to_string("purchase.html", {"base_url":settings.BASE_URL})
    email = EmailMessage(
        'Transacción Exitosa',
        html,
        'contacto@mlsparts.shop',
        [order.user.email],
        reply_to=['contact@mlsparts.shop'],
        headers={'Message-ID': 'foo'},
    )
    email.content_subtype = 'html'
    email.attach(f'orden-{order.id}.pdf', receipt, 'text/pdf')
    email.send(fail_silently=True)



    