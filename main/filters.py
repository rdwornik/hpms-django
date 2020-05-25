import django_filters

from django.conf import settings
from django.db.models import Q
from django_filters import rest_framework as rest_filters
from main import models

SERVER_CHOICES = [(id, server) for id, server in models.HeaderValue.objects.filter(Q(header_names__header_name=settings.SERVER_NAME)).distinct().values_list()] 
SERVER_CHOICES.insert(0, ('', 'Select server'))
  
VISITOR_IP_CHOICES = [(id, value) for id, value in models.HeaderValue.objects.filter(Q(header_names__header_name=settings.VISITORS_IP)).distinct().values_list()]
VISITOR_IP_CHOICES.insert(0, ('', '----'))

class TransactionsFilter(django_filters.FilterSet):
    ip = django_filters.ChoiceFilter(method="ip_filter",choices=VISITOR_IP_CHOICES)
    server = django_filters.ChoiceFilter(method="server_filter",choices=SERVER_CHOICES)
    assigned_tags = django_filters.ModelMultipleChoiceFilter(required=False,queryset=models.LogsTag.objects.all())
    time = django_filters.DateTimeFromToRangeFilter(required=False)

    class Meta:
        model = models.Transaction
        fields = ["time","assigned_tags","ip","server",]    
    def ip_filter(self, queryset, name, value):
        return queryset.filter(Q(name__header_name=settings.VISITORS_IP) & Q(value=value))
    def server_filter(self, queryset, name, value):
        return queryset.filter(Q(name__header_name=settings.SERVER_NAME) & Q(value=value))
    
class ChartFilter(rest_filters.FilterSet):
    time = rest_filters.DateTimeFromToRangeFilter(required=False)
    assigned_tags = rest_filters.ModelMultipleChoiceFilter(required=False,queryset=models.LogsTag.objects.all())
    class Meta:
        model = models.Transaction
        fields = ["time","assigned_tags"]

        
    