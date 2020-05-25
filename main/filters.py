import django_filters

from django.conf import settings
from django.db.models import Q
from django_filters import rest_framework as rest_filters
from main import models

from django.forms import ModelForm, TextInput, SelectMultiple, Select
from django.urls import reverse_lazy

class TransactionsFilter(django_filters.FilterSet):
    visitor_ip =    django_filters.ModelMultipleChoiceFilter(required=False,to_field_name="visitor_ip",method='filter_visitor_ip',queryset=models.Transaction.objects.order_by('visitor_ip').distinct('visitor_ip'))
    server =        django_filters.ModelChoiceFilter(required=False,to_field_name="server",method='filter_server',queryset=models.Transaction.objects.order_by('server').distinct('server'))
    assigned_tags = django_filters.ModelMultipleChoiceFilter(required=False,queryset=models.LogsTag.objects.all())
    time =          django_filters.DateTimeFromToRangeFilter(required=False)
    
    def __init__(self, *args, **kwargs):
        super(TransactionsFilter, self).__init__(*args, **kwargs)
        self.form.fields['server'].label_from_instance = self.server_label_from_instance
        self.form.fields['visitor_ip'].label_from_instance = self.visitor_ip_label_from_instance

    @staticmethod
    def server_label_from_instance(obj):
        return "%s" % obj.server
    
    @staticmethod
    def visitor_ip_label_from_instance(obj):
        return "%s" % obj.visitor_ip
    
    def filter_server(self, queryset, name, value):
        return queryset.filter(Q(server=value.server))
        
    def filter_visitor_ip(self, queryset, name, value):
        return queryset.filter(visitor_ip__in=[ q.visitor_ip for q in value ]) if value else queryset
    
    class Meta:
        model = models.Transaction
        fields = ["time","assigned_tags","visitor_ip","server"]
    
class ChartFilter(rest_filters.FilterSet):
    time =              rest_filters.DateTimeFromToRangeFilter(required=False)
    assigned_tags =     rest_filters.ModelMultipleChoiceFilter(required=False,queryset=models.LogsTag.objects.all())
    class Meta:
        model = models.Transaction
        fields = ["time","assigned_tags"]