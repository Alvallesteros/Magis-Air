from django import forms

class DateFilterForm(forms.Form):
    filter_date = forms.DateField(
        label='Filter by Date', 
        widget=forms.DateInput(attrs={'type': 'date'}),
        required=False
        )