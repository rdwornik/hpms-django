import logging

from django import forms
from django.views.generic.edit import FormView
from django.forms import ModelForm, TextInput

from dal import autocomplete
from main import models

logger = logging.getLogger(__name__)

class TagsActionSelectForm(forms.Form):
    ACTIONS = (
        ("delete_selected","Deleted selected Tags"),
        ("empty","---------------")
        )
    select = forms.TypedChoiceField(choices=ACTIONS)

class TagForm(ModelForm):
    class Meta:
        model = models.LogsTag
        fields = "__all__"
        localized_fields = "__all__"
        widgets = {
            "tag": TextInput(),
            "value_cryteria" : TextInput()
        }

class TagsAutocompleteForm(forms.ModelForm):
    tags = forms.ModelChoiceField(
        queryset=models.LogsTag.objects.all(),
        widget=autocomplete.ModelSelect2(url='tags-autocomplete')
    )

    class Meta:
        model = models.LogsTag
        fields = ['tags']