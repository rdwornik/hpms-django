from django import forms
from django.views.generic.edit import FormView
from django.forms import ModelForm, TextInput
from main.models import LogsTag

class TagsActionSelectForm(forms.Form):
    ACTIONS = (
        ("delete_selected","Deleted selected Tags"),
        ("add_selected","Add Tag"),
        ("edit_selected","Edit selected Tag"),
        ("empty","Select Action")
        )
    select = forms.TypedChoiceField(choices=ACTIONS)

    def get_actions_index(self, selected_action):
        return self.ACTIONS.index(selected_action)
class TagForm(ModelForm):
    class Meta:
        model = LogsTag
        fields = '__all__'
        localized_fields = '__all__'
        widgets = {
            'tag': TextInput(),
            'value_cryteria' : TextInput()
        }