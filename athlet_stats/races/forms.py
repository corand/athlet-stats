from django import forms
from django.forms import ModelForm
from .models import Race

class RaceForm(ModelForm):
    class Meta:
    	model = Race
    	fields = ['name','month','week']
    	widgets = { 
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'month': forms.Select(attrs={'class': 'form-control'}),
            'week': forms.Select(attrs={'class': 'form-control'}),
        }