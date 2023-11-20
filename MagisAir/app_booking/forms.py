from django import forms

class NameSearchForm(forms.Form):
    first_name = forms.CharField(label='First Name', max_length=255, required=False, widget=forms.TextInput(attrs={'required' : 'True'}))
    last_name = forms.CharField(label='Last Name', max_length=255, required=False, widget=forms.TextInput(attrs={'required' : 'True'})) 

class DateRangeForm(forms.Form):
    start_date = forms.DateField(label='Start Date', widget=forms.DateInput(attrs={'type': 'date'}), required=False)
    end_date = forms.DateField(label='End Date', widget=forms.DateInput(attrs={'type': 'date'}), required=False)

class IdSearchForm(forms.Form):
    passenger_id = forms.CharField(label='Passenger ID', max_length=255, required=False, widget=forms.TextInput(attrs={'required' : 'True'}))