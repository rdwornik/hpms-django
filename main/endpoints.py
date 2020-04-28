from rest_framework import viewsets, generics
from rest_framework.response import Response

from main import serializers, models, filters

from django.db.models import Count, DateTimeField, TimeField, DateField
from django.db.models.functions import TruncDay, TruncHour

from django_filters.rest_framework import DjangoFilterBackend
from django.forms.widgets import NumberInput, HiddenInput, TextInput, DateTimeInput
from django.contrib.postgres.forms  import RangeWidget, DateTimeRangeField

class ChartViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = models.Transaction.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_class  = filters.ChartFilter

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        timedelta = queryset.first().time - queryset.last().time
        if timedelta.days == 0:
            queryset = queryset.annotate(x=TruncHour('time', output_field=TimeField())).values('x').order_by().annotate(y=Count('x')).distinct() 
            s = serializers.HoursSerializer(queryset,many=True)
        else:
            queryset = queryset.annotate(x=TruncDay('time', output_field=DateField())).values('x').order_by().annotate(y=Count('x')).distinct() 
            s = serializers.DaysSerializer(queryset,many=True)
        data = {
            'data':s.data,
            'label' : [1,2,3]
        }
        return Response(data)
class LogsLogViewSet(viewsets.ModelViewSet):
    queryset = models.LogsLog.objects.all()
    serializer_class = serializers.HoneypotRequestSerializer

    def list(self, request, *args, **kwargs):
        serializer = serializers.LogsLogSerializer(self.get_queryset().order_by("transaction").reverse(),many=True)
        return Response(serializer.data)   

