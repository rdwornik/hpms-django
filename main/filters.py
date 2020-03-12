import django_filters

from datetime import datetime, timedelta
from django.forms.widgets import NumberInput, HiddenInput, TextInput
from django import forms as django_forms
from main import models
from django.db.models import Q

class TransactionsFilter(django_filters.FilterSet):
    time = django_filters.NumberFilter(method='time_filter',widget=NumberInput(attrs={'placeholder': 'hours'}))
    ip = django_filters.NumberFilter(method='ip_filter',field_name='value',widget=HiddenInput())

    def time_filter(self, queryset, name, value):
        time_threshold = datetime.now() - timedelta(hours=int(value))
        return queryset.filter(time__gt=time_threshold)

    def ip_filter(self, queryset, name, value):
        return queryset.exclude(Q(name__header_name='VISITORS_IP') & ~Q(value_id=value))

    @property
    def qs(self):
        parent = super().qs
        return parent.order_by('-transaction').distinct('transaction')

    class Meta:
        model = models.LogsLog
        fields = ['time','transaction','name']


