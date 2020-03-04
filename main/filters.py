import django_filters

from datetime import datetime, timedelta
from django.forms.widgets import NumberInput
from main import models


class TransactionsFilter(django_filters.FilterSet):

    time = django_filters.NumberFilter(method='since_added',widget=NumberInput(attrs={'placeholder': 'hours'}))
    def since_added(self, queryset, name, value):
        time_threshold = datetime.now() - timedelta(hours=int(value))
        return queryset.filter(time__gt=time_threshold)

    class Meta:
        model = models.LogsLog
        fields = ['time','transaction','name']
