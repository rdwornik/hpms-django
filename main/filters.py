import django_filters

from datetime import datetime, timedelta
from django.forms.widgets import NumberInput, HiddenInput, TextInput
from django import forms as django_forms
from django.conf import settings
from django.db.models import Q
from django.urls import reverse
from django.http import HttpRequest
from dal import autocomplete
from main import models, views
from urllib.request import urlopen
from .forms import get_choice_list

SERVER_CHOICES = [(id, server) for id, server in enumerate(
    models.LogsLog.objects.values_list("server",flat=True).distinct())]
VISITOR_IP_CHOICES = [(id, value) for value, id in get_choice_list()]

class TransactionsFilter(django_filters.FilterSet):
    time = django_filters.NumberFilter(method="time_filter",
                                       widget=NumberInput(attrs={"placeholder": "Select hours from now"}))
    
    ip = django_filters.ChoiceFilter(method="ip_filter",
                                     choices=VISITOR_IP_CHOICES,
                                     widget=autocomplete.ListSelect2(url="visitors-ip-list-autocomplete",
                                                                     attrs={"data-placeholder" : "Select Visitor IP"}))

    server = django_filters.ChoiceFilter(method="server_filter",
                                         choices=SERVER_CHOICES,
                                         empty_label="Select Server")
    
    tags = django_filters.ModelChoiceFilter(method="tags_filter",
                                            queryset=models.LogsTag.objects.all(),
                                            widget=autocomplete.ModelSelect2(url="tags-autocomplete", 
                                                                      attrs={"data-placeholder" : "Select Tag"}))
    
    def time_filter(self, queryset, name, value):
        time_threshold = datetime.now() - timedelta(hours=int(value))
        return queryset.filter(time__gt=time_threshold)

    def ip_filter(self, queryset, name, value):
        return queryset.exclude(Q(name__header_name=settings.VISITORS_IP) & ~Q(value_id=value))
    
    def server_filter(self, queryset, name, value):
        server = next(iter([s[1] for s in SERVER_CHOICES if int(value) == s[0]] or []), None)
        return queryset.filter(Q(server=server))

    def tags_filter(self,queryset, name, value):
        transaction = models.LogsTagAssign.objects.filter(Q(tag=value)).values_list("transaction", flat=True)
        return queryset.filter(transaction__in=transaction)
    
    @property
    def qs(self):
        parent = super().qs
        return parent.order_by("-transaction").distinct("transaction")
       
    class Meta:
        model = models.LogsLog
        fields = ["time","server","tags"]
        
class TagsFilter(django_filters.FilterSet):
    tags = django_filters.ModelChoiceFilter(queryset=models.LogsTag.objects.all(),
                                            widget=autocomplete.ModelSelect2(url="tags-autocomplete", 
                                                                      attrs={"data-placeholder" : "Select Tag"}))
    class Meta:
        model = models.LogsTag
        fields = ["tags"]
    