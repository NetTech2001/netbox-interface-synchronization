from django import forms


class ComponentComparisonForm(forms.Form):
    add_to_device = forms.BooleanField(required=False)
    remove_from_device = forms.BooleanField(required=False)
