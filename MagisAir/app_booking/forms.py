from django import forms

class NameSearchForm(forms.Form):
    first_name = forms.CharField(max_length=255, required=True)
    last_name = forms.CharField(max_length=255, required=True) 