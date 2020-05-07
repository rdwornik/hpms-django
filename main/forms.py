from django import forms
from django.views.generic.edit import FormView
from django.forms import ModelForm, TextInput, SelectMultiple
from django.db.models import Q
from django.conf import settings
from main import models, widgets
from django.forms.widgets import DateTimeInput, SplitDateTimeWidget
from django.urls import reverse_lazy

from django.contrib.postgres.forms  import RangeWidget, DateTimeRangeField
from main import widgets
def get_visitor_ip_choice_list():
    return  models.HeaderValue.objects.filter(Q(header_names__header_name=settings.VISITORS_IP)).distinct().values_list('header_value','id') 
SERVER_CHOICES = [(id, server) for id, server in 
                models.HeaderValue.objects.filter(Q(header_names__header_name=settings.SERVER_NAME)).distinct().values_list()] 

TAGS_CHOICES = [(tag['id'], tag['tag']) for tag in models.LogsTag.objects.values('id','tag')] 
import datetime
class CustomWidget(SplitDateTimeWidget):
    def decompress(self, value):
        print("hello")
        print(value)
        if value:
            return [value.date(), value.time()]
        return [None, None]
class ActivityForm(forms.Form):
    time_after = forms.DateTimeField(required=False,
                                     input_formats=["%Y-%m-%d %H:%M"],
                                    widget=widgets.DateTimePickerInput())
    time_before = forms.DateTimeField(required=False,
                                      input_formats=["%Y-%m-%d %H:%M"],
                                    widget=widgets.DateTimePickerInput())
    
    assigned_tags = forms.ModelMultipleChoiceField(required=False,
                                          queryset=models.LogsTag.objects.all(),
                                          widget=SelectMultiple(attrs={"multiple":"multiple",
                                                                       "url-endpoint-select":reverse_lazy("tag-list")}))
    def clean(self):
        cleaned_data = super().clean()
        if cleaned_data.get("time_after") > cleaned_data.get("time_before"):
            msg = "Time after can't be bigger then time before"
            self.add_error('time_after',msg)
        return self.cleaned_data

class TagsActionSelectForm(ModelForm):
    ACTIONS = (
        ("delete_selected","Deleted selected tags"),
        ("search","Search tags"),
        ("empty","Select Action")
        )
    select = forms.TypedChoiceField(choices=ACTIONS)
    tags = forms.CharField(required=False,widget=forms.TextInput(attrs={'placeholder': 'Search'}))
    
    class Meta:
        model = models.LogsTag
        fields = ['tags']

class TagForm(ModelForm):
    class Meta:
        model = models.LogsTag
        fields = "__all__"
        localized_fields = "__all__"
        widgets = {
            "tag": TextInput(),
            "value_cryteria" : TextInput()
        }