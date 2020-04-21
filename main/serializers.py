from django.db import transaction
from django.core.exceptions import ObjectDoesNotExist

from rest_framework import serializers

from main import models

class TagsSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.LogsTagAssign

class ChartSerializer(serializers.ModelSerializer):
    tags = TagsSerializer(many=True,read_only=True)
    class Meta:
        model = models.LogsLog
        exclude = ['id','name','value']
        # read_only_fields = ['transaction', 'time']

class HttpHeaderSerializer(serializers.Serializer):
    name = serializers.CharField(required=False, allow_blank=True)
    value = serializers.CharField(required=False, allow_blank=True)

class HoneypotRequestSerializer(serializers.Serializer):
    headers = HttpHeaderSerializer(many=True,write_only=True)
    def save(self):
        http_headers = self.validated_data.pop("headers")
        headers = [
            (
            models.HeaderName.objects.get_or_create(header_name=header["name"]),
            models.HeaderValue.objects.get_or_create(header_value=header["value"])
            )
            for header in http_headers
            ]
        try:
            with transaction.atomic():
                trans = models.LogsLog.objects.latest().transaction + 1
                logs = [ models.LogsLog(
                        transaction=trans,
                        name = header_name[0],
                        value = header_value[0],
                    )for header_name, header_value in headers ]
                logs_created = models.LogsLog.objects.bulk_create(logs,ignore_conflicts=True)
        except models.LogsLog.DoesNotExist:
            logs = [ models.LogsLog(
                        name = header_name[0],
                        value = header_value[0],
                        )for header_name, header_value in headers ]
            logs_created = models.LogsLog.objects.bulk_create(logs,ignore_conflicts=True)
        models.LogsTagAssign.objects.assign_tags(logs_created)
        
class ValueSerializer(serializers.RelatedField):
    def to_representation(self, value):
        return value.header_value
    class Meta:
        model = models.HeaderValue

class NameSerializer(serializers.RelatedField):
    def to_representation(self, value):
        return value.header_name
    class Meta:
        model = models.HeaderName

class LogsLogSerializer(serializers.ModelSerializer):
    name = NameSerializer(read_only=True)
    value = ValueSerializer(read_only=True)

    class Meta:
        model = models.LogsLog
        fields = [
            "name",
            "value",
            "transaction",
            "time",
        ]