import django_filters
import ast

from django.conf import settings
from django.db.models import Q
from django_filters import rest_framework as rest_filters
from main import models

from django.forms import ModelForm, TextInput, SelectMultiple, Select
from django.urls import reverse_lazy
from main import forms



class NoteFilter(django_filters.FilterSet):
    visitor_ip =    django_filters.CharFilter(required=False,method='visitor_ip_filter',widget=Select(attrs={"data-url":reverse_lazy("note-visitor-ip-list"),"tags":"true"}))
    title =         django_filters.CharFilter(required=False,method='title_filter',widget=Select(attrs={"data-url":reverse_lazy("note-titles-list"),"tags":"true"}))
    transaction =   django_filters.NumberFilter(required=False)
        
    def visitor_ip_filter(self, queryset, name, value):
        return queryset.filter(visitor_ip__istartswith=value)
    def title_filter(self, queryset, name, value):
        return queryset.filter(title__istartswith=value)
        
    class Meta:
        model = models.LogsNote
        fields = ["visitor_ip","title","transaction"]

class TransactionsFilter(django_filters.FilterSet):
    visitor_ip =    django_filters.CharFilter(required=False,method='visitor_ip_filter',widget=SelectMultiple(attrs={"data-url":reverse_lazy("visitor-ip-list"),"tags":"false"}))
    assigned_tags = django_filters.ModelMultipleChoiceFilter(required=False,queryset=models.LogsTag.objects.all())
    server =        django_filters.ModelChoiceFilter(required=False,method='server_filter',queryset=models.HeaderValue.objects.filter(Q(header_names__header_name=settings.SERVER_NAME)).distinct())
    time =          django_filters.DateTimeFromToRangeFilter(required=False)

    def __init__(self, *args, **kwargs):
        super(TransactionsFilter, self).__init__(*args, **kwargs)
        self.form.fields['server'].label_from_instance = self.server_label_from_instance

    @staticmethod
    def server_label_from_instance(obj):
        return "%s" % obj.header_value
    
    def visitor_ip_filter(self, queryset, name, value):
        return queryset.filter(Q(name__header_name=settings.VISITOR_IP) & Q(value__in=ast.literal_eval(value)))
    def server_filter(self, queryset, name, value):
        return queryset.filter(Q(name__header_name=settings.SERVER_NAME) & Q(value=value))
    
    class Meta:
        model = models.Transaction
        fields = ["time","assigned_tags"]
        form = forms.DateTimeRangeValidationForm
    
class ChartFilter(rest_filters.FilterSet):
    time =              rest_filters.DateTimeFromToRangeFilter(required=False)
    assigned_tags =     rest_filters.ModelMultipleChoiceFilter(required=False,queryset=models.LogsTag.objects.all())
    class Meta:
        model = models.Transaction
        fields = ["time","assigned_tags"]
        form = forms.DateTimeRangeValidationForm