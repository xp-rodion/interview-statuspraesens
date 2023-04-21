from django import forms


class EmailFileForm(forms.Form):
    file = forms.FileField()
