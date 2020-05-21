import datetime

from django import forms
from django.forms import ModelForm, TextInput, SelectMultiple, Select
from django.db.models import Q
from django.conf import settings
from django.urls import reverse_lazy
from main import models, widgets

SERVER_CHOICES = [(id, server) for id, server in models.HeaderValue.objects.filter(Q(header_names__header_name=settings.SERVER_NAME)).distinct().values_list()] 
SERVER_CHOICES.insert(0, ('', 'Select server'))
  
VISITOR_IP_CHOICES = [(value, id) for id, value in models.HeaderValue.objects.filter(Q(header_names__header_name=settings.VISITORS_IP)).distinct().values_list('header_value','id')]
VISITOR_IP_CHOICES.insert(0, ('', '----'))

#TODO Clean modules and code review
#TODO write extra tests
#TODO sortowanie
#TODO style tabel w oddzielnym pliku css

class TransactionBasicForm(forms.Form):
    time_after = forms.DateTimeField(   required=False,
                                        input_formats=["%Y-%m-%d %H:%M"],
                                        widget=widgets.DateTimePickerInput())
    time_before = forms.DateTimeField(  required=False,
                                        input_formats=["%Y-%m-%d %H:%M"],
                                        widget=widgets.DateTimePickerInput())
    
    assigned_tags = forms.ModelMultipleChoiceField( required=False,
                                                    queryset=models.LogsTag.objects.all(),
                                                    widget=SelectMultiple(attrs={   "multiple":"multiple",
                                                                                    "display-name":"tags",
                                                                                    "url-endpoint-select":reverse_lazy("tag-list")}))
    def clean(self):
        cleaned_data = super().clean()
        if cleaned_data.get("time_after") > cleaned_data.get("time_before"):
            msg = "Time after can't be bigger then time before"
            self.add_error('time_after',msg)
        return self.cleaned_data
class TransactionsForm(TransactionBasicForm):
    ip = forms.ChoiceField( required=False,
                            choices=VISITOR_IP_CHOICES,
                            widget=Select(attrs={"display-name":"ip",
                                                 "url-endpoint-select":reverse_lazy("ip-list")}))
    server = forms.ChoiceField(required=False,
                               choices=SERVER_CHOICES)
class TagsActionSelectForm(ModelForm):
    ACTIONS = (
        ("delete_selected","Deleted selected tags"),
        ("search","Search tags"),
        )
    select = forms.TypedChoiceField(choices=ACTIONS)
    tags = forms.CharField( required=False,
                            widget=forms.TextInput(attrs={"autocomplete":"off",
                                                          "data-url": reverse_lazy("tag-names-list")}))
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
class NoteForm(ModelForm):
    transaction = forms.ModelChoiceField(queryset=models.Transaction.objects.all(),disabled=True,required=False)
    ip = forms.ModelChoiceField(queryset=models.HeaderValue.objects.all(),disabled=True,required=False)
    
    field_order=["ip","transaction","title","content"]
    
    class Meta:
        model = models.LogsNote
        fields = "__all__"
        localized_fields = "__all__"
        widgets = {
            "title" : TextInput(),
        }
    
    def __init__(self, *args, **kwargs):
        super(NoteForm, self).__init__(*args, **kwargs)
        self.fields['transaction'].label_from_instance = self.transaction_label_from_instance
        self.fields['ip'].label_from_instance = self.ip_label_from_instance

    @staticmethod
    def transaction_label_from_instance(obj):
        return "%s" % obj.pk
    
    @staticmethod
    def ip_label_from_instance(obj):
        return "%s" % obj.header_value
    
class NotesActionSelectForm(ModelForm):
    ACTIONS = (
        ("delete_selected","Deleted selected notes"),
        ("search","Search notes"),
        )
    select = forms.TypedChoiceField(choices=ACTIONS)
    title = forms.CharField(required=False,
                            widget=forms.TextInput(attrs={"autocomplete":"off",
                                                          "data-url": reverse_lazy("note-titles-list")}))
    class Meta:
        model = models.LogsNote
        fields = ['title']