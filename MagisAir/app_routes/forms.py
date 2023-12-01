from django import forms


class RouteForm(forms.Form):
    origin_name = forms.CharField(label="Origin", max_length=255)
    destination_name = forms.CharField(label="Destination", max_length=255)
