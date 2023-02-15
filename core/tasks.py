from typing import List
from celery import shared_task
from django.core.mail import EmailMessage
from core.controllers.receipt_controller import generate_receipt
from django.conf import settings
from django.template.loader import render_to_string
from django.core.files.uploadedfile import SimpleUploadedFile
from core.models.export_file import ExportFile
from core.models.store import Store
from core.utils.image import generate_picture_to_django_user, generate_picture_to_store
from core.models.order import Order
from core.controllers.sendgrid_controller import send_email_template,send_email_template_file
from core.controllers.export_controllers.chart import get_chart_csv_bytes, get_contacts_csv_bytes, get_orders_csv_bytes, get_products_csv_bytes, save_model,get_asistances_csv_bytes
from core.controllers.notification_controller import create_notification
from django.contrib.auth import get_user_model
from core.models.assistance import Assistance
from core.models.product import Products
from core.choices.model_choices import SendgridTemplateChoices
import base64

User = get_user_model()

@shared_task
def export_products(ids:List[int], user_email):
    user = User.objects.get(email=user_email)
    if not user.store: return
    queryset = Products.objects.filter(id__in=ids)
    data = get_products_csv_bytes(queryset)
    e_f : ExportFile = save_model(data, "exportacion_productos.csv", user=user)
    create_notification(
            content="Su Archivo de exportación está listo!", 
            entity_name="export_file", 
            entity_id=f"{e_f.id}", 
            group=f"store_{user.store.name}"
        )
@shared_task
def export_assistances(ids:List[int], user_email):
    user = User.objects.get(email=user_email)
    if not user.store: return
    queryset = Assistance.objects.filter(id__in=ids)
    data = get_asistances_csv_bytes(queryset)
    e_f : ExportFile = save_model(data, "exportacion_asistencias.csv", user=user)
    create_notification(
            content="Su Archivo de exportación está listo!", 
            entity_name="export_file", 
            entity_id=f"{e_f.id}", 
            group=f"store_{user.store.name}"
        )
    
@shared_task
def export_chart(chart_data, yearly, user_email):
    user = User.objects.get(email=user_email)
    if not user.store: return
    data = get_chart_csv_bytes(chart_data,yearly)
    e_f : ExportFile = save_model(data, "exportacion_dashboard.csv", user=user)
    create_notification(
            content="Su Archivo de exportación está listo!", 
            entity_name="export_file", 
            entity_id=f"{e_f.id}", 
            group=f"store_{user.store.name}"
        )
    
@shared_task
def export_contacts(ids:List[int], user_email):
    user = User.objects.get(email=user_email)
    if not user.store: return
    queryset = User.objects.filter(id__in=ids)
    data = get_contacts_csv_bytes(queryset)
    e_f : ExportFile = save_model(data, "exportacion_contactos.csv", user=user)
    create_notification(
            content="Su Archivo de exportación está listo!", 
            entity_name="export_file", 
            entity_id=f"{e_f.id}", 
            group=f"store_{user.store.name}"
        )
    
@shared_task
def export_orders(ids:List[int], user_email):
    user = User.objects.get(email=user_email)
    if not user.store: return
    queryset = Order.objects.filter(id__in=ids)
    data = get_orders_csv_bytes(queryset)
    e_f : ExportFile = save_model(data, "exportacion_ordenes.csv", user=user)
    create_notification(
            content="Su Archivo de exportación está listo!", 
            entity_name="export_file", 
            entity_id=f"{e_f.id}", 
            group=f"store_{user.store.name}"
        )

@shared_task
def send_email_template_task(to_emails:List[str],template_id:str, template_data:dict):
    send_email_template(to_emails, template_id, template_data)

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
    
    send_email_template_file([order.user.email],SendgridTemplateChoices.COMPRA_EXITOSA,{'name':order.user.first_name}, receipt, filename=f'Recibo {order.id}')
    # html = render_to_string("purchase.html", {"base_url":settings.BASE_URL})
    # email = EmailMessage(
    #     'Transacción Exitosa',
    #     html,
    #     'contacto@mlsparts.shop',
    #     [order.user.email],
    #     reply_to=['contact@mlsparts.shop'],
    #     headers={'Message-ID': 'foo'},
    # )
    # email.content_subtype = 'html'
    # email.attach(f'orden-{order.id}.pdf', receipt, 'text/pdf')
    # email.send()



    