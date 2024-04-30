from django import forms
from django.forms.widgets import PasswordInput, TextInput


class SearchForm(forms.Form):
    search = forms.CharField(widget=TextInput(attrs={'placeholder': 'Search', 'class': 'form-control', 'aria-label':'Search'}),label="")