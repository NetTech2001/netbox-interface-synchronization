from django import forms


class InterfaceComparisonForm(forms.Form):
    add_to_device = forms.BooleanField(required=False)
    remove_from_device = forms.BooleanField(required=False)
