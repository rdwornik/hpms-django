from django.db import transaction
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import serializers
from rest_framework import (
    permissions,
    viewsets
)
from rest_framework.response import Response


from .models import LogsLog, HeaderName, HeaderValue

class HttpHeaderSerializer(serializers.Serializer):
    name = serializers.CharField(required=False, allow_blank=True)
    value = serializers.CharField(required=False, allow_blank=True)

class HoneypotRequestSerializer(serializers.ModelSerializer):
    headers = HttpHeaderSerializer(many=True,write_only=True)
    class Meta:
        model = LogsLog
        exclude = ['id','transaction','name','value']

    def create(self, validated_data):
        http_headers = validated_data.pop("headers")
        headers = [
        (HeaderName.objects.get_or_create(header_name=item['name']),
        HeaderValue.objects.get_or_create(header_value=item['value']))
        for item in http_headers
        ]
        try:
            with transaction.atomic():
                trans = LogsLog.objects.latest().transaction + 1
                logs = [LogsLog(transaction=trans,
                        name = item[0][0],
                        value = item[1][0],
                        **validated_data
                    )for item in headers ]
                obj = LogsLog.objects.bulk_create(logs)
        except LogsLog.DoesNotExist:
            logs = [LogsLog(name = item[0][0],
                        value = item[1][0],
                        **validated_data
                        )for item in headers ]
            obj = LogsLog.objects.bulk_create(logs)
        return obj[0]

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
            'name',
            'value',
            'transaction',
        ]

class LogsLogViewSet(viewsets.ModelViewSet):
    queryset = LogsLog.objects.all()
    serializer_class = HoneypotRequestSerializer

    # def get_serializer(self, *args, **kwargs):
    #     """ if an array is passed, set serializer to many """
    #     if isinstance(kwargs.get('data', {}), list):
    #         kwargs['many'] = True
    #     return super(LogsLogViewSet, self).get_serializer(*args, **kwargs)


    def list(self, request, *args, **kwargs):
        serializer = LogsLogSerializer(self.get_queryset().order_by('transaction').reverse(),many=True)
        return Response(serializer.data)
