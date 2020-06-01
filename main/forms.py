import datetime

from django import forms
from django.db.models import Q
from django.conf import settings
from django.urls import reverse_lazy
from main import models

from django.contrib.postgres.fields import DateTimeRangeField
from django.contrib.postgres import forms as psql_forms
from django.forms import inlineformset_factory, modelform_factory,formset_factory,modelformset_factory

#TODO Clean modules and code review
#TODO write extra tests
#TODO sortowanie
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

class LogsTagForm(forms.ModelForm):     
    class Meta:
        model = models.LogsTag
        exclude = ["cryterias"]
        localized_fields = "__all__"
        widgets = {
            "tag_name": forms.TextInput(),
        }

TagCryteriaFormSet = modelformset_factory(models.TagCryteria,
                                          fields=("name_cryteria","value_cryteria"),
                                          extra=1,
                                          min_num=1, 
                                          validate_min=True,
                                          can_delete=True,
                                          widgets = {"value_cryteria": forms.TextInput()})

class NoteForm(forms.ModelForm):
    transaction =   forms.IntegerField(disabled=True,required=False)
    visitor_ip =            forms.CharField(disabled=True)
    
    field_order=    ["visitor_ip","transaction","title","content"]
    class Meta:
        model = models.LogsNote
        exclude = ['id','transactions']
        localized_fields = "__all__"
        widgets = {
            "title": forms.TextInput(),
        }
    
class TagsActionSelectForm(forms.ModelForm):
    ACTIONS =  (("delete_selected","Deleted selected tags"),
                ("search","Search tags"))

    select = forms.TypedChoiceField(choices=ACTIONS)
    tag_names = forms.CharField( required=False,
                            widget=forms.TextInput(attrs={"autocomplete":"off",
                                                          "data-url": reverse_lazy("tag-names-list")}))
    class Meta:
        model = models.LogsTag
        fields = ['tag_names']