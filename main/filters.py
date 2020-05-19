import django_filters

from datetime import datetime, timedelta
from django.forms.widgets import NumberInput, HiddenInput, TextInput, DateTimeInput, SelectMultiple
from django import forms as django_forms
from django.conf import settings
from django.db.models import Q
from django.urls import reverse
from django.http import HttpRequest
from main import models
from urllib.request import urlopen
from .forms import get_visitor_ip_choice_list
from tempus_dominus.widgets import DatePicker, TimePicker, DateTimePicker
from . import widgets
from django_filters import rest_framework as rest_filters

SERVER_CHOICES = [(id, server) for id, server in 
                models.HeaderValue.objects.filter(Q(header_names__header_name=settings.SERVER_NAME)).distinct().values_list()] 

from django.contrib.postgres.forms  import RangeWidget, DateTimeRangeField
from django.forms import Select
from django.urls import reverse_lazy
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

        
    