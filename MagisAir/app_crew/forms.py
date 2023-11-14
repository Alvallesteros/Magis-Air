from django import forms

class DateFilterForm(forms.Form):
    filter_date = forms.DateField(label='Filter by Date', required=False, # removes error message lol
                                  widget=forms.DateInput(attrs={'type': 'date',
                                                                'required': 'True' # keep requiredness of date even if field mismo is not required
                                                                })
                                )