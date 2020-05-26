import django_filters
import ast

from django.conf import settings
from django.db.models import Q
from django_filters import rest_framework as rest_filters
from main import models

from django.forms import ModelForm, TextInput, SelectMultiple, Select
from django.urls import reverse_lazy
from main import forms

class TransactionsFilter(django_filters.FilterSet):
    server =        django_filters.ModelChoiceFilter(required=False,to_field_name="server",method='filter_server',queryset=models.Transaction.objects.order_by('server').distinct('server'))
    assigned_tags = django_filters.ModelMultipleChoiceFilter(required=False,queryset=models.LogsTag.objects.all())
    time =          django_filters.DateTimeFromToRangeFilter(required=False)
    visitor_ip =    django_filters.CharFilter(required=False,method='filter_visitor_ip',widget=SelectMultiple(attrs={"data-url":reverse_lazy("visitor-ip-list")}))

    def __init__(self, *args, **kwargs):
        super(TransactionsFilter, self).__init__(*args, **kwargs)
        self.form.fields['server'].label_from_instance = self.server_label_from_instance

    @staticmethod
    def server_label_from_instance(obj):
        return "%s" % obj.server
    
    def filter_server(self, queryset, name, value):
        return queryset.filter(Q(server=value.server))
        
    def filter_visitor_ip(self, queryset, name, value):
        return queryset.filter(visitor_ip__in=ast.literal_eval(value))
    
    class Meta:
        model = models.Transaction
        fields = ["time","assigned_tags","visitor_ip","server"]
        form = forms.DateTimeRangeValidationForm
    
class ChartFilter(rest_filters.FilterSet):
    time =              rest_filters.DateTimeFromToRangeFilter(required=False)
    assigned_tags =     rest_filters.ModelMultipleChoiceFilter(required=False,queryset=models.LogsTag.objects.all())
    class Meta:
        model = models.Transaction
        fields = ["time","assigned_tags"]
        form = forms.DateTimeRangeValidationForm