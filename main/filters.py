import django_filters
import ast

from django.conf import settings
from django.db.models import Q
from django_filters import rest_framework as rest_filters , fields
from django.forms import SelectMultiple, Select, NumberInput, MultiWidget, TextInput, ModelChoiceField, CharField
from django.urls import reverse_lazy
from main import forms, models

class CharRangeFilter(rest_filters.RangeFilter):
    class CharRangeField(fields.RangeField):
        def __init__(self, *args, **kwargs):
            super().__init__(widget=MultiWidget(widgets=[Select(attrs={"data-url":reverse_lazy("header-name-list"),"tags":"true"}), TextInput(attrs={"placeholder":"Type header value"})]),fields=(
                CharField(),
                CharField()
            ), *args, **kwargs)
    field_class = CharRangeField

class NoteFilter(django_filters.FilterSet):
    visitor_ip =    django_filters.CharFilter(required=False,method='visitor_ip_filter',widget=Select(attrs={"data-url":reverse_lazy("note-visitor-ip-list"),"tags":"true"}))
    title =         django_filters.CharFilter(required=False,method='title_filter',widget=Select(attrs={"data-url":reverse_lazy("note-titles-list"),"tags":"true"}))
    transaction =   django_filters.NumberFilter(required=False,widget=NumberInput(attrs={"placeholder":"Select transaction"}))

    def visitor_ip_filter(self, queryset, name, value):
        return queryset.filter(visitor_ip__istartswith=value)
    def title_filter(self, queryset, name, value):
        return queryset.filter(title__istartswith=value)
        
    class Meta:
        model = models.LogsNote
        fields = ("visitor_ip","title","transaction")

class TagFilter(django_filters.FilterSet):
    tag_name =         django_filters.CharFilter(required=False,method='tag_name_filter',widget=Select(attrs={"data-url":reverse_lazy("tag-names-list"),"tags":"true"}))
    
    def tag_name_filter(self, queryset, name, value):
        return queryset.filter(tag_name__istartswith=value)
    class Meta:
        model = models.LogsTag
        fields = ("tag_name",)

class TransactionsFilter(django_filters.FilterSet):
    visitor_ip =    django_filters.CharFilter(required=False,method='visitor_ip_filter',widget=SelectMultiple(attrs={"data-url":reverse_lazy("visitor-ip-list"),"tags":"false"}))
    assigned_tags = django_filters.ModelMultipleChoiceFilter(required=False,queryset=models.LogsTag.objects.all())
    server =        django_filters.ModelChoiceFilter(required=False,method='server_filter',queryset=models.HeaderValue.objects.filter(Q(header_names__header_name=settings.SERVER_NAME)).distinct())
    time =          django_filters.DateTimeFromToRangeFilter(required=False)
    header =        CharRangeFilter(required=False,method='header_filter')

    def __init__(self, *args, **kwargs):
        super(TransactionsFilter, self).__init__(*args, **kwargs)
        self.form.fields['assigned_tags'].label_from_instance = self.assigned_tags_label_from_instance
        
    @staticmethod
    def assigned_tags_label_from_instance(obj):
        return "%s" % obj.tag_name
    
    def visitor_ip_filter(self, queryset, name, value):
        return queryset.filter(Q(name__header_name=settings.VISITOR_IP) & Q(value__in=ast.literal_eval(value)))
    def server_filter(self, queryset, name, value):
        return queryset.filter(Q(name__header_name=settings.SERVER_NAME) & Q(value=value))
    def header_filter(self, queryset, name, value):
        if(value.start and value.stop):
            return queryset.filter(Q(name__header_name=value.start) & Q(value__header_value=value.stop))
        else:
            return queryset 

    class Meta:
        model = models.Transaction
        fields = ("time","assigned_tags")
        form = forms.DateTimeRangeValidationForm
    
class ChartFilter(rest_filters.FilterSet):
    time =              rest_filters.DateTimeFromToRangeFilter(required=False)
    assigned_tags =     rest_filters.ModelMultipleChoiceFilter(required=False,queryset=models.LogsTag.objects.all())
    
    def __init__(self, *args, **kwargs):
        super(ChartFilter, self).__init__(*args, **kwargs)
        self.form.fields['assigned_tags'].label_from_instance = self.assigned_tags_label_from_instance

    @staticmethod
    def assigned_tags_label_from_instance(obj):
        return "%s" % obj.tag_name
    class Meta:
        model = models.Transaction
        fields = ("time","assigned_tags")
        form = forms.DateTimeRangeValidationForm