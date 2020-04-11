import logging

from django import forms
from django.views.generic.edit import FormView
from django.forms import ModelForm, TextInput
from main.models import LogsTag


logger = logging.getLogger(__name__)

class TagsActionSelectForm(forms.Form):
    ACTIONS = (
        ("delete_selected","Deleted selected Tags"),
        ("empty","---------------")
        )
    select = forms.TypedChoiceField(choices=ACTIONS)

class TagForm(ModelForm):
    class Meta:
        model = LogsTag
        fields = "__all__"
        localized_fields = "__all__"
        widgets = {
            "tag": TextInput(),
            "value_cryteria" : TextInput()
        }