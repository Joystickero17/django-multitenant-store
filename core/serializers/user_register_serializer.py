from rest_framework import serializers,exceptions
from core.utils.model_choices import UserTypeRegisterChoices
from core.models.category import Category
from django.contrib.auth import get_user_model


User = get_user_model()

class UserRegisterSerializer(serializers.Serializer):
    name = serializers.CharField()
    last_name = serializers.CharField()
    email =  serializers.EmailField()
    password =  serializers.CharField()
    password_repeat = serializers.CharField()
    rif = serializers.CharField(required=False)
    user_type = serializers.ChoiceField(choices=UserTypeRegisterChoices.CHOICES)
    company_name = serializers.CharField(required=False)
    company_employee_number = serializers.CharField(required=False)
    company_anual_income = serializers.FloatField(required=False)
    company_main_category =  serializers.PrimaryKeyRelatedField(queryset=Category.objects.all(),required=False)
    email_send_consent =  serializers.BooleanField()

    def validate(self, attrs):
        try:
            user_exists = User.objects.get(email=attrs["email"])
            raise exceptions.ValidationError("Ese correo ya esta siendo utilizado, asegurese de poner los datos correctamente")
        except User.DoesNotExist as e:
            pass

        user_type = attrs.get("user_type")
        if attrs.get("password") != attrs.get("password_repeat"):
            raise exceptions.ValidationError("Las contraseñas no coinciden")
        if not user_type == UserTypeRegisterChoices.SHOP:
            return super().validate(attrs)
        company_data = [
                    attrs.get("company_name"),
                    attrs.get("company_employee_number"),
                    attrs.get("company_main_category"),
                ]
        print(company_data)
        if not all(company_data):
            raise exceptions.ValidationError("Faltan Datos de compañia, por favor revise el formulario e intente de nuevo")
        return super().validate(attrs)