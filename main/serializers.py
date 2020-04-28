import datetime

from rest_framework import serializers
from main import models

class DaysSerializer(serializers.Serializer):
    x = serializers.DateField()
    y = serializers.IntegerField()

    
class HoursSerializer(serializers.Serializer):
    x = serializers.TimeField()
    y = serializers.IntegerField()
class TransactionModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Transaction
        fields = '__all__'
class ValueSerializer(serializers.RelatedField):
    def to_representation(self, value):
        return value.header_value
    def to_internal_value(self, data):
        return self.queryset.get_or_create(header_value=data)[0]
    class Meta:
        model = models.HeaderValue

class NameSerializer(serializers.RelatedField):
    def to_representation(self, value):
        return value.header_name
    def to_internal_value(self, data):
        return self.queryset.get_or_create(header_name=data)[0]
    class Meta:
        model = models.HeaderName

class TransactionSerializer(serializers.RelatedField):
    def to_representation(self, value):
        return value.transaction
    class Meta:
        model = models.Transaction

class LogsLogSerializer(serializers.ModelSerializer):
    name = NameSerializer(queryset=models.HeaderName.objects.all())
    value = ValueSerializer(queryset=models.HeaderValue.objects.all())
    transaction = TransactionSerializer(required=False,read_only=True)
    
    class Meta:
        model = models.LogsLog
        fields = '__all__'

class HoneypotRequestSerializer(serializers.Serializer):
    headers = LogsLogSerializer(many=True)
    def save(self):
        t = models.Transaction.objects.create()
        logs = [ models.LogsLog(transaction=t, **h) for h in self.validated_data['headers'] ]
        logs_created = models.LogsLog.objects.bulk_create(logs,ignore_conflicts=True)
        models.LogsTagAssign.objects.assign_tags_on_logs_created(logs_created)