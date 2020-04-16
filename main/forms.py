import logging

from django import forms
from django.views.generic.edit import FormView
from django.forms import ModelForm, TextInput
from django.db.models import Q
from django.conf import settings

from dal import autocomplete
from main import models

logger = logging.getLogger(__name__)

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
        
def get_choice_list():
    return  models.LogsLog.objects.filter(
                                        Q(name__header_name=settings.VISITORS_IP)
                                     ).values_list(
                                        "value__header_value","value_id"
                                     ).distinct()
                                    
class TransactionsAutocompleteForm(forms.ModelForm):
    tags = forms.ModelChoiceField(
        queryset=models.LogsTag.objects.all(),
        widget=autocomplete.ModelSelect2(url='tags-autocomplete'),
    )
    
    visitors_ip = autocomplete.Select2ListChoiceField(
        choice_list=get_choice_list,
        widget=autocomplete.ListSelect2(url="visitors-ip-list-autocomplete"),
    )

    class Meta:
        model = models.LogsTag
        fields = ['tags']