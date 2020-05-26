import datetime

from django import forms
from django.forms import ModelForm, TextInput, SelectMultiple, Select
from django.db.models import Q
from django.conf import settings
from django.urls import reverse_lazy
from main import models

from django.contrib.postgres.fields import DateTimeRangeField
from django.contrib.postgres import forms as psql_forms


#TODO Clean modules and code review
#TODO write extra tests
#TODO sortowanie
#TODO style tabel w oddzielnym pliku css
#TODO order headers alfabetcznie
class DateTimeRangeValidationForm(forms.Form):
    def clean(self):
        cleaned_data = super().clean()
        if  cleaned_data["time"]:
            time_after = cleaned_data["time"].start
            time_before = cleaned_data["time"].stop
            if time_after > time_before:
                msg = "Time after can't be bigger then time before"
                self.add_error('time',msg)
        return self.cleaned_data

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


class TagsActionSelectForm(ModelForm):
    ACTIONS =  (("delete_selected","Deleted selected tags"),
                ("search","Search tags"))

    select = forms.TypedChoiceField(choices=ACTIONS)
    tags = forms.CharField( required=False,
                            widget=forms.TextInput(attrs={"autocomplete":"off",
                                                          "data-url": reverse_lazy("tag-names-list")}))
    class Meta:
        model = models.LogsTag
        fields = ['tags']

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