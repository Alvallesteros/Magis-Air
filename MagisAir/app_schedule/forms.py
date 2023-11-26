from django import forms


class DateFilterForm(forms.Form):
    filter_date = forms.DateField(
<<<<<<< HEAD
        label='Filter by Date',
        required=False,
        widget=forms.DateInput(attrs={'type': 'date', 'required': 'True'}),
    )
=======
        label='Filter by Date', 
        widget=forms.DateInput(attrs={'type': 'date'}),
        required=False
        )
>>>>>>> views-schedule-frontend
