import logging
from django.shortcuts import render
from datetime import datetime, timedelta
from django import forms as django_forms
from django.db import models as django_models
import django_filters
from django_filters.views import FilterView

from main import models
# Create your views here.

logger = logging.getLogger(__name__)

class DateInput(django_forms.DateInput):
    input_type = 'date'
class LogsLogFilter(django_filters.FilterSet):

    time = django_filters.NumberFilter(method='since_added')

    def since_added(self, queryset, name, value):
        print(name)
        print(value)
        time_threshold = datetime.now() - timedelta(hours=22)
        print(time_threshold)
        return queryset.filter(time__gt=time_threshold)

    class Meta:
        model = models.LogsLog
        fields = ['time']




