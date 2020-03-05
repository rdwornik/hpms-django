from django import forms


class MaskForm(forms.Form):
    mask = forms.IntegerField