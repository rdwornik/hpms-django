import django_filters

from datetime import datetime, timedelta
from django.forms.widgets import NumberInput, HiddenInput, TextInput
from django import forms as django_forms
from django.conf import settings
from django.db.models import Q
from django.urls import reverse

from dal import autocomplete
from main import models

SERVER_CHOICES = [(id, choice) for id, choice in enumerate(
    models.LogsLog.objects.values_list("server",flat=True).distinct())]

class TransactionsFilter(django_filters.FilterSet):
    time = django_filters.NumberFilter(method="time_filter",
                                       widget=NumberInput(attrs={"placeholder": "hours"}))
    ip = django_filters.NumberFilter(method="ip_filter",
                                     field_name="value",
                                     widget=HiddenInput())

    server = django_filters.ChoiceFilter(method="server_filter",
                                         choices=SERVER_CHOICES,
                                         empty_label="Select Server")
    
    tags = django_filters.ModelChoiceFilter(method="tags_filter",
                                     queryset=models.LogsTag.objects.all(),
                                     widget=autocomplete.ModelSelect2(url="tags-autocomplete")
                                     )
    
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