import django_filters

from django.conf import settings
from django.db.models import Q
from django_filters import rest_framework as rest_filters
from main import models

class TransactionsFilter(django_filters.FilterSet):
    ip = django_filters.ChoiceFilter(method="ip_filter")
    server = django_filters.ChoiceFilter(method="server_filter")
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

        
    