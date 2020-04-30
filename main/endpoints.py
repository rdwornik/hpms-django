from rest_framework import viewsets, generics
from rest_framework.response import Response

from main import  models, filters,utils, serializers

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
        ###TODO handle empty query set request on submit make filtr transactions time on id rather than on time
        date1, date2 = utils.date_order(queryset.first().time, queryset.last().time)
        td = date2 - date1  
        range = [key for key, value in utils.range.items() if value(td) == True][0]                                                
        trunc_func, field_type, serializer = utils.trunc_methods[range]
        label_type = range
        queryset = queryset.annotate(x=trunc_func('time', output_field=field_type())).values('x').order_by().annotate(y=Count('pk')) 
        data = serializer(queryset,many=True).data
        data = {
            'data':data,
            'label' : label_type,
            'displayFormats' : utils.display_format
        }
        return Response(data)
class LogsLogViewSet(viewsets.ModelViewSet):
    queryset = models.LogsLog.objects.all()
    serializer_class = serializers.HoneypotRequestSerializer

    def list(self, request, *args, **kwargs):
        serializer = serializers.LogsLogSerializer(self.get_queryset().order_by("transaction").reverse(),many=True)
        return Response(serializer.data)   

