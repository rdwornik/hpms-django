from rest_framework import viewsets, generics
from rest_framework.response import Response

from main import  models, filters,utils, serializers

from django.db.models import Count, DateTimeField, TimeField, DateField
from django.db.models.functions import TruncDay, TruncHour
from django.conf import settings
from django.db.models import Q

from django_filters.rest_framework import DjangoFilterBackend
from django.forms.widgets import NumberInput, HiddenInput, TextInput, DateTimeInput
from django.contrib.postgres.forms  import RangeWidget, DateTimeRangeField
from dateutil.relativedelta import relativedelta
import datetime
class VisitorList(viewsets.ReadOnlyModelViewSet):
    serializer_class = serializers.HeaderValueModelSerializer  
    class Meta:
        model = models.HeaderValue
    def get_queryset(self):
        qs = models.HeaderValue.objects.filter(Q(header_names__header_name=settings.VISITORS_IP)).distinct() 
        q = self.request.query_params.get('q', None)
        if q is not None:
            qs = qs.filter(header_value__istartswith=q)
        return qs
    
class LogsTagList(viewsets.ReadOnlyModelViewSet):
    serializer_class = serializers.LogsTagModelSerializer  
    class Meta:
        model = models.LogsTag
    def get_queryset(self):
        qs = models.LogsTag.objects.all()
        q = self.request.query_params.get('q', None)
        if q is not None:
            qs = qs.filter(tag__istartswith=q)
        return qs
    
class TagsList(viewsets.ReadOnlyModelViewSet):
    serializer_class = serializers.HeaderValueModelSerializer  
    class Meta:
        model = models.HeaderValue
    def get_queryset(self):
        qs = models.HeaderValue.objects.filter(Q(header_names__header_name=settings.VISITORS_IP)).distinct() 
        q = self.request.query_params.get('q', None)
        if q:
            qs = qs.filter(header_value__istartswith=q)     
        return qs

#TODO Ogarnąć walidacje na on load
class ChartViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = models.Transaction.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_class  = filters.ChartFilter
    
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        # time_0 = (datetime.datetime.now() + relativedelta(years=-1)) if request.GET.get('time_0') is None else datetime.datetime.fromisoformat(request.GET.get('time_0'))
        # time_1 =  datetime.datetime.now() if request.GET.get('time_1') is None else datetime.datetime.fromisoformat(request.GET.get('time_1'))
        # print(request.GET['time_after'],request.GET['time_before'])
        date1, date2 = utils.date_order(datetime.datetime.fromisoformat(request.GET['time_after']),datetime.datetime.fromisoformat(request.GET['time_before']))
        td = date2 - date1  
        range = [key for key, value in utils.range.items() if value(td) == True][0]                                                
        trunc_func = utils.trunc_methods[range]
        label_type = range
        queryset = queryset.annotate(x=trunc_func('time', output_field=DateTimeField())).values('x').order_by().annotate(y=Count('pk')) 
        data = serializers.ChartSerializer(queryset,many=True).data
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

