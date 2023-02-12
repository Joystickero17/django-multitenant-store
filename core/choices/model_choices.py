
class ProductStorageChoices:
    TIENDA_FISICA = 'tienda_fisica'
    ALMACEN = 'almacen'
    CHOICES = [
        (TIENDA_FISICA, "Tienda Física de la tienda"),
        (ALMACEN, "Almacen de la tienda")
    ]

class SendgridTemplateChoices:
    GC_AMAZON = 'd-852fba4c7fe142a48156cc43db25dd6f'
    PASSWORD_EMAIL_RESET= 'd-1a8daef8c5174445b15f7662fe361bb0'
    BIENVENIDO_INVITADO='d-b8114559af0b48798fc200e21a4ebc82'
    CHOICES = [
        (GC_AMAZON, "Envio de gift Card de Amazon"),
        (PASSWORD_EMAIL_RESET, "Envio de link para resetaear el password"),
        (BIENVENIDO_INVITADO, "Bienvenido Usuario invitado con foto de Toreto")
    ]


class PersonType:
    NATURAL = "N"
    JURIDICA = "J"
    GUBERNAMENTAL = "G"
    EXTRANJERA = "E"
    CHOICES = [
        (NATURAL, "Persona Natural"),
        (JURIDICA, "Persona Juridica, Empresa"),
        (GUBERNAMENTAL, "Ente Gubernamental"),
        (EXTRANJERA, "Persona Extranjera Legal")
    ]

class DocumentType:
    CEDULA = "CEDULA"
    LICENCIA_CONDUCIR = "LICENCIA_CONDUCIR"
    PASAPORTE = "PASAPORTE"
    RIF = "RIF"
    CHOICES = [
        (CEDULA, "Cédula de identidad"),
        (LICENCIA_CONDUCIR, "Licencia de Conducir"),
        (PASAPORTE, "Pasaporte"),
        (RIF, "Registro de Información Fiscal")
        ]

class RoleChoices:
    WEBSITE_OWNER = "website_owner"
    STORE_OWNER = "store_owner"
    STORE_OPERATOR = "store_operator"
    RANDOM_ROLE = "random_role"
    FREELANCE = "freelance"
    CUSTOMER = "customer"
    BASE_USER = "base_user"
    CHOICES = [
        (WEBSITE_OWNER, "Dueño del sitio Web"),
        (BASE_USER, "Usuario Sin rol"),
        (STORE_OWNER, "Dueño de Tienda"),
        (STORE_OPERATOR, "Operador de tienda"),
        (FREELANCE, "Freelance"),
        (CUSTOMER, "Cliente"),
        (RANDOM_ROLE, "Rol de Prueba"),
        (BASE_USER, "Usuario sin rol"),
    ]