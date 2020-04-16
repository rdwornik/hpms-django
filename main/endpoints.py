from django.db import transaction
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import serializers
from rest_framework import (
    permissions,
    viewsets
)
from rest_framework.response import Response

from .models import LogsLog, HeaderName, HeaderValue, LogsTagAssign

class HttpHeaderSerializer(serializers.Serializer):
    name = serializers.CharField(required=False, allow_blank=True)
    value = serializers.CharField(required=False, allow_blank=True)

class HoneypotRequestSerializer(serializers.ModelSerializer):
    headers = HttpHeaderSerializer(many=True,write_only=True)
    class Meta:
        model = LogsLog
        exclude = ["id","transaction","name","value"]

    def create(self, validated_data):
        http_headers = validated_data.pop("headers")
        headers = [
            (
            HeaderName.objects.get_or_create(header_name=header["name"]),
            HeaderValue.objects.get_or_create(header_value=header["value"])
            )
            for header in http_headers
            ]
        try:
            with transaction.atomic():
                trans = LogsLog.objects.latest().transaction + 1
                logs = [ LogsLog(
                        transaction=trans,
                        name = header_name[0],
                        value = header_value[0],
                        **validated_data
                    )for header_name, header_value in headers ]
                logs_created = LogsLog.objects.bulk_create(logs,ignore_conflicts=True)
        except LogsLog.DoesNotExist:
            logs = [ LogsLog(
                        name = header_name[0],
                        value = header_value[0],
                        **validated_data
                        )for header_name, header_value in headers ]
            logs_created = LogsLog.objects.bulk_create(logs,ignore_conflicts=True)
        LogsTagAssign.objects.assign_tags(logs_created)
        return logs_created[0]

class ValueSerializer(serializers.RelatedField):
    def to_representation(self, value):
        return value.header_value
    class Meta:
        model = HeaderValue

class NameSerializer(serializers.RelatedField):
    def to_representation(self, value):
        return value.header_name
    class Meta:
        model = HeaderName

class LogsLogSerializer(serializers.ModelSerializer):
    name = NameSerializer(read_only=True)
    value = ValueSerializer(read_only=True)

    class Meta:
        model = LogsLog
        fields = [
            "name",
            "value",
            "transaction",
            "time",
            "server"
        ]

class LogsLogViewSet(viewsets.ModelViewSet):
    queryset = LogsLog.objects.all()
    serializer_class = HoneypotRequestSerializer

    def list(self, request, *args, **kwargs):
        serializer = LogsLogSerializer(self.get_queryset().order_by("transaction").reverse(),many=True)
        return Response(serializer.data)