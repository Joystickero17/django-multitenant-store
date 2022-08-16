
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
    BASE_USER = "BASE_USER"
    CHOICES = [
        (BASE_USER, "Usuario Sin rol")
    ]