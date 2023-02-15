from typing import List
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail,To, Subject,Content
from python_http_client.exceptions import HTTPError
from sendgrid.helpers.mail import (Attachment, FileContent, FileName, FileType, Disposition)
from django.conf import settings
import base64


# HEADERS = {
#     "Authorization":f"Bearer {}"
# }
TOKEN = settings.SENDGRID_API_KEY

def send_email_template_file(to_emails:List[str],template_id:str, template_data:dict, file_data:bytes, **kwargs):
    to_emails_instances = [To(
        email=item,
        name="Sin Nombre",
        p=0
    ) for item in to_emails]
    message = Mail(from_email="contacto@mlsparts.shop")
    message.to = to_emails_instances
    message.template_id = template_id
    message.dynamic_template_data = template_data
    sg = SendGridAPIClient(TOKEN)
    encoded_file = base64.b64encode(file_data).decode()
    attachedFile = Attachment(
    FileContent(encoded_file),
    FileName(f'{kwargs.get("filename") or "Archivo Sin Nombre"}.pdf'),
    FileType('application/pdf'),
    Disposition('attachment')
    )
    message.attachment = attachedFile
    try:
        response = sg.send(message)
        print(response.status_code)
        print(response.body)
        print(response.headers)
    except HTTPError as e:
        print(e.to_dict)

def send_email_template(to_emails:List[str],template_id:str, template_data:dict):
    to_emails_instances = [To(
        email=item,
        name="Sin Nombre",
        p=0
    ) for item in to_emails]
    message = Mail(from_email="contacto@mlsparts.shop")
    message.to = to_emails_instances
    message.template_id = template_id
    message.dynamic_template_data = template_data
    sg = SendGridAPIClient(TOKEN)
    try:
        response = sg.send(message)
        print(response.status_code)
        print(response.body)
        print(response.headers)
    except HTTPError as e:
        print(e.to_dict)

def send_plain_email(to_emails:List[str], subject:str, content: str):
    to_emails_instances = [To(
        email=item,
        name="Sin Nombre",
        p=0
    ) for item in to_emails]
    message = Mail(from_email="contacto@mlsparts.shop")
    message.to = to_emails_instances
    message.subject = Subject(subject)
    message.content = [
        Content(
        mime_type="text/html",
        content=f"{content}"
        )
        ]
    sg = SendGridAPIClient(TOKEN)
    try:
        response = sg.send(message)
        print(response.status_code)
        print(response.body)
        print(response.headers)
    except HTTPError as e:
        print(e.to_dict)