from django import forms

class NameSearchForm(forms.Form):
    first_name = forms.CharField(max_length=255, required=True)
    last_name = forms.CharField(max_length=255, required=True) 

class DateRangeForm(forms.Form):
    start_date = forms.DateField(label='Start Date', widget=forms.DateInput(attrs={'type': 'date'}), required=False)
    end_date = forms.DateField(label='End Date', widget=forms.DateInput(attrs={'type': 'date'}), required=False)