from django.db import transaction
from django.core.exceptions import ObjectDoesNotExist

from rest_framework import serializers

from main import models

class HttpHeaderSerializer(serializers.Serializer):
    name = serializers.CharField(required=False, allow_blank=True)
    value = serializers.CharField(required=False, allow_blank=True)

class HoneypotRequestSerializer(serializers.ModelSerializer):
    headers = HttpHeaderSerializer(many=True,write_only=True)
    class Meta:
        model = models.LogsLog
        exclude = ["id","transaction","name","value"]

    def create(self, validated_data):
        http_headers = validated_data.pop("headers")
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
                        **validated_data
                    )for header_name, header_value in headers ]
                logs_created = models.LogsLog.objects.bulk_create(logs,ignore_conflicts=True)
        except models.LogsLog.DoesNotExist:
            logs = [ models.LogsLog(
                        name = header_name[0],
                        value = header_value[0],
                        **validated_data
                        )for header_name, header_value in headers ]
            logs_created = models.LogsLog.objects.bulk_create(logs,ignore_conflicts=True)
        models.LogsTagAssign.objects.assign_tags(logs_created)
        return logs_created[0]

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
            "server"
        ]