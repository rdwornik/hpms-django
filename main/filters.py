import django_filters

from datetime import datetime, timedelta
from django.forms.widgets import NumberInput, HiddenInput, TextInput, DateTimeInput
from django import forms as django_forms
from django.conf import settings
from django.db.models import Q
from django.urls import reverse
from django.http import HttpRequest
from dal import autocomplete
from main import models
from urllib.request import urlopen
from .forms import get_visitor_ip_choice_list
from tempus_dominus.widgets import DatePicker, TimePicker, DateTimePicker
from . import widgets

SERVER_CHOICES = [(id, server) for id, server in 
                models.HeaderValue.objects.filter(Q(header_names__header_name=settings.SERVER_NAME)).distinct().values_list()] 
VISITOR_IP_CHOICES = [(value, id) for id, value in get_visitor_ip_choice_list()]

from django.contrib.postgres.forms  import RangeWidget, DateTimeRangeField

class TransactionsFilter(django_filters.FilterSet):
    ip = django_filters.ChoiceFilter(method="ip_filter",
                                     choices=VISITOR_IP_CHOICES,
                                     widget=autocomplete.ListSelect2(url="visitors-ip-list-autocomplete",
                                                                     attrs={"data-placeholder" : "Filter Visitor IP"}))

    server = django_filters.ChoiceFilter(method="server_filter",
                                         choices=SERVER_CHOICES,
                                         empty_label="Select Server")
    
    tags = django_filters.ModelChoiceFilter(method="tags_filter",
                                            queryset=models.LogsTag.objects.all(),
                                            widget=autocomplete.ModelSelect2(url="tags-autocomplete", 
                                                                             attrs={"data-placeholder" : "Filter Tag"}))
    time = django_filters.DateTimeFromToRangeFilter(widget=RangeWidget(base_widget=widgets.DateTimePickerInput()))
    class Meta:
        model = models.Transaction
        fields = ["time","server","ip","tags"]    
    def ip_filter(self, queryset, name, value):
        return queryset.filter(Q(name__header_name=settings.VISITORS_IP) & Q(value=value))
    def server_filter(self, queryset, name, value):
        return queryset.filter(Q(name__header_name=settings.SERVER_NAME) & Q(value=value))
    def tags_filter(self,queryset, name, value):
        return queryset.filter(assigned_tags=value)