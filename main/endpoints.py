from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from django.db.models import Count, DateTimeField
from django.conf import settings
from django.db.models import Q
from django_filters.rest_framework import DjangoFilterBackend
from main import  models, filters,utils, serializers
from dateutil.relativedelta import relativedelta

import datetime
#TODO Placeholdey dodac
class LogsNotesTitleList(viewsets.ReadOnlyModelViewSet):
    serializer_class = serializers.LogsNotesTitleModelSerializer
    authentication_classes = (SessionAuthentication, BasicAuthentication)
    permission_classes = [IsAuthenticated] 
    class Meta:
        model = models.LogsNote
    def get_queryset(self):
        qs = models.LogsNote.objects.all()
        title = self.request.query_params.get('title', None)
        q = self.request.query_params.get('q', None)
        if q is not None:
            qs = qs.filter(title__istartswith=q)
        elif title :
            qs = qs.filter(title=title)
        return qs
    
class LogsNotesVisitorIpList(viewsets.ReadOnlyModelViewSet):
    serializer_class = serializers.LogsNotesVisitorIpModelSerializer
    authentication_classes = (SessionAuthentication, BasicAuthentication)
    permission_classes = [IsAuthenticated]
    class Meta:
        model = models.LogsNote
    def get_queryset(self):
        qs = models.LogsNote.objects.all().order_by('visitor_ip').distinct('visitor_ip')
        visitor_ip = self.request.query_params.get('visitor_ip', None)
        q = self.request.query_params.get('q', None)
        if q is not None:
            qs = qs.filter(visitor_ip__istartswith=q)
        elif visitor_ip :
            qs = qs.filter(visitor_ip=visitor_ip)
        return qs
    
class VisitorIpList(viewsets.ReadOnlyModelViewSet):
    serializer_class = serializers.HeaderValueModelSerializer
    authentication_classes = (SessionAuthentication, BasicAuthentication)
    permission_classes = [IsAuthenticated]
    class Meta:
        model = models.HeaderValue
    def get_queryset(self):
        qs = models.HeaderValue.objects.filter(Q(header_names__header_name=settings.VISITOR_IP)).distinct() 
        visitor_ip = self.request.query_params.getlist('visitor_ip', None)
        q = self.request.query_params.get('q', None)
        if q :
            qs = qs.filter(header_value__istartswith=q)
        elif visitor_ip :
            qs = qs.filter(pk__in=visitor_ip)
        return qs
    
class LogsTagList(viewsets.ReadOnlyModelViewSet):
    serializer_class = serializers.LogsTagModelSerializer  
    authentication_classes = (SessionAuthentication, BasicAuthentication)
    permission_classes = [IsAuthenticated] 
    class Meta:
        model = models.LogsTag
    def get_queryset(self):
        qs = models.LogsTag.objects.all()
        q = self.request.query_params.get('q', None)
        if q is not None:
            qs = qs.filter(tag__istartswith=q)
        return qs
    
class LogsTagNamesList(viewsets.ReadOnlyModelViewSet):
    authentication_classes = (SessionAuthentication, BasicAuthentication)
    permission_classes = [IsAuthenticated] 
    class Meta:
        model = models.LogsTag
    def get_queryset(self):
        qs = models.LogsTag.objects.all()
        term = self.request.query_params.get('term', None)
        if term is not None:
            qs = qs.filter(tag__istartswith=term)
        return qs
    
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        data = serializers.LogsTagNamesModelSerializer(queryset,many=True).data
        names = [list(name.values())[0] for name in data]
        return Response(names)
    
class ChartViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = models.Transaction.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_class  = filters.ChartFilter
    authentication_classes = (SessionAuthentication, BasicAuthentication)
    permission_classes = [IsAuthenticated]
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        time_after =    datetime.datetime.fromisoformat(request.GET.get('time_after'))  if request.GET.get('time_after')    else (datetime.datetime.now() + relativedelta(years=-1))  
        time_before =   datetime.datetime.fromisoformat(request.GET.get('time_before')) if request.GET.get('time_before')   else datetime.datetime.now() 
        td = time_before - time_after       
        time_range = [key for key, value in utils.time_range.items() if value(td) == True][0]                                                
        trunc_func = utils.trunc_methods_chart[time_range]
        queryset = queryset.annotate(x=trunc_func('time', output_field=DateTimeField())).values('x').order_by('x').annotate(y=Count('pk')) 
        data = serializers.ChartSerializer(queryset,many=True).data
        data = {
            'data':data,
            'label' : time_range,
            'displayFormats' : utils.display_format
        }
        return Response(data)

class LogsLogViewSet(viewsets.ModelViewSet):
    queryset = models.LogsLog.objects.all()
    serializer_class = serializers.HoneypotRequestSerializer
    authentication_classes = (BasicAuthentication,)
    def list(self, request, *args, **kwargs):
        serializer = serializers.LogsLogSerializer(self.get_queryset().order_by("transaction").reverse(),many=True)
        return Response(serializer.data)