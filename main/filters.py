import django_filters

from datetime import datetime, timedelta
from django.forms.widgets import NumberInput, HiddenInput, TextInput
# from django.forms import GenericIPAddressField,DateInput
from django import forms as django_forms
from main import models

class IPAdressInput(django_forms.GenericIPAddressField):
    unpack_ipv4=True
    
    def __init__(self, *args, **kwargs):
        self.is_hidden = False
        self.attrs={'type':'hidden'}
        super(IPAdressInput, self).__init__(*args, **kwargs)
    

class TransactionsFilter(django_filters.FilterSet):

    time = django_filters.NumberFilter(method='since_added',widget=NumberInput(attrs={'placeholder': 'hours'}))
    ip = django_filters.CharFilter(field_name='value_id',method='ip_adress',widget=HiddenInput(),lookup_expr='value_id__exact')
    
    def since_added(self, queryset, name, value):
        time_threshold = datetime.now() - timedelta(hours=int(value))
        return queryset.filter(time__gt=time_threshold)
    def ip_adress(self, queryset, name, value):
        print('hello')
        print(value)
        value=5
        # self.current_user
        return queryset

    # @property
    # def current_user(self):
    #     print(self.request)
    #     return getattr(self.request, 'user', None)



        

    class Meta:
        model = models.LogsLog
        fields = ['time','transaction','name']
