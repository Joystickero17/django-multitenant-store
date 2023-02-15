from rest_framework import serializers
from core.models.export_file import ExportFile


class ExportFileSerializer(serializers.ModelSerializer):
    s3_file_name=serializers.SerializerMethodField()
    class Meta:
        model = ExportFile
        fields = '__all__'

    def get_s3_file_name(self,obj):
        if not obj.file: return
        return obj.file.name.replace('exports/','')