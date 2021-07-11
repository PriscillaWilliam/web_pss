from django import forms
from django.forms import ModelForm

from django.db.models import CharField, Value

from django.db.models.functions import Concat

class SearchForm(forms.Form):

    StaffIdList = forms.ModelChoiceField(empty_label='', required=True,
        widget=forms.Select(attrs={'class': 'form-control'}))


