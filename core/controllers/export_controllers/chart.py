from io import StringIO
from core.models.export_file import ExportFile
from django.core.files.base import ContentFile
from core.serializers.order_serializer import ExportContactSerializer, ExportOrderSerializer, PrivateUserSerializer
from core.serializers.assistance_serializer import AssistanceSerializer, ExportAssistanceSerializer
import csv

from core.serializers.product_serializer import ExportProductSerializer

def save_model(file:StringIO, name:str, **kwargs):
    e_f = ExportFile()
    e_f.filename = name
    e_f.user = kwargs.get("user")
    e_f.file.save(name, ContentFile(file.getvalue().encode()))
    return e_f


def get_products_csv_bytes(queryset):
    output = StringIO()
    headers = [
            "id",
            "name",
            "category_name",
            "brand_name",
            "description",
            "product_slug",
            "rating",
            "price",
            "thumbnail_url",
            "quantity",
            "store_name",
            "condition_display",
            "product_storage_address",
            ]
    true_headers = {            
            "id":"Id de Producto",
            "name":"Nombre del producto",
            "category_name":"Categoria",
            "brand_name":"Marca",
            "description":"Descripcion",
            "product_slug":"Slug",
            "rating":"Calificaciones",
            "price":"Precio",
            "thumbnail_url":"url de Miniatura",
            "quantity":"Cantidad",
            "store_name":"Tienda",
            "condition_display":"Condicion",
            "product_storage_address":"Direccion del Almacen",
        }
        
    data = ExportProductSerializer(queryset, many=True).data
    writer = csv.DictWriter(output,fieldnames=headers, delimiter=';')
    writer.writerow(true_headers)
    writer.writerows(data)
    return output

def get_asistances_csv_bytes(queryset):
    output = StringIO()
    headers = [
            "id",
            "freelance_email",
            "customer_email",
            "completed_display",
            "feedback_display",
        ]
    true_headers = {
            "id":"Numero de la Asistencia",
            "customer_email":"Email del Cliente",
            "freelance_email":"Email del Freelance",
            'completed_display': 'Completada',
            'feedback_display':'Calificacion',
            
        }
        
    data = ExportAssistanceSerializer(queryset, many=True).data
    writer = csv.DictWriter(output,fieldnames=headers, delimiter=';')
    writer.writerow(true_headers)
    writer.writerows(data)
    return output

def get_orders_csv_bytes(queryset):
    """
    Retorna los bytes de un csv para la data de los charts en estadisticas
    """
    output = StringIO()
    headers = [
            'id',
            'payment_method',
            'receipt_url',
            'delivery_type_display',
            'created_at',
            'user_email',
            'payment_status_display',
            'total_amount'
        ]
    true_headers = {
            "id":"Numero de la Orden",
            "user_email":"Email del Cliente",
            "receipt_url":"Url del recibo",
            "payment_status_display":'Estado del pago',
            "payment_method":"Metodo de pago",
            "delivery_type_display":"Tipo de entrega",
            "created_at":"Fecha",
            "total_amount":"Monto de la orden"
        }
        
    data = ExportOrderSerializer(queryset, many=True).data
    writer = csv.DictWriter(output,fieldnames=headers, delimiter=';')
    writer.writerow(true_headers)
    writer.writerows(data)
    return output


def get_contacts_csv_bytes(queryset):
    """
    Retorna los bytes de un csv para la data de los charts en estadisticas
    """
    output = StringIO()
    headers = [
            "email",
            "phone_number",
            "store_name",
            "first_name",
            "last_name",
            "total_orders"
        ]
    true_headers = {
            "email":"Email",
            "phone_number":"Numero de Telefono",
            "store_name":"Tienda del Usuario",
            "first_name":"Nombres",
            "last_name":"Apellidos",
            "total_orders":"Ordenes Totales"
        }
        
    data = ExportContactSerializer(queryset, many=True).data
    writer = csv.DictWriter(output,fieldnames=headers, delimiter=';')
    writer.writerow(true_headers)
    writer.writerows(data)
    return output

def get_chart_csv_bytes(chart_data:dict, yearly=False)->StringIO:
    """
    Retorna los bytes de un csv para la data de los charts en estadisticas
    """
    output = StringIO()
    headers = [
        "Mes" if yearly else "Dia",
        "Dolares",
        "Total de Ventas",
        "Total de Freelancers",
        "Total de Visitas",
        "Productos Registrados",
        "Usuarios",
        "Reseñas"
        ]
    
    writer = csv.writer(output, delimiter=';')
    writer.writerow(headers)
    
    for index, item in enumerate(chart_data["chart"].items()):
        if index == 0:
            writer.writerow([item[0],item[1],chart_data['total_sales_count'], chart_data['total_freelancers'], chart_data['visits'], chart_data['products'], chart_data['users'], chart_data['reviews']])
        else:
            writer.writerow([item[0],item[1]])
    return output
