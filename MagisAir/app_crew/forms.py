from django import forms

class DateFilterForm(forms.Form):
    start_date = forms.DateField(label='Start Date', required=False, # removes error message lol
                                  widget=forms.DateInput(attrs={'type': 'date',
                                                                'required': 'True' # keep requiredness of date even if field mismo is not required
                                                                })
                                )
    end_date = forms.DateField(label='End Date', required=False, # removes error message lol
                                  widget=forms.DateInput(attrs={'type': 'date',
                                                                'required': 'True' # keep requiredness of date even if field mismo is not required
                                                                })
                                )