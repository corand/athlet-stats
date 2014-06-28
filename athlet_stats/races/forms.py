from django import forms
from django.forms import ModelForm
from .models import Race,Edition

class RaceForm(ModelForm):
    class Meta:
    	model = Race
    	fields = ['name','month','week']
    	widgets = { 
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'month': forms.Select(attrs={'class': 'form-control'}),
            'week': forms.Select(attrs={'class': 'form-control'}),
        }

class EditionForm(ModelForm):
	class Meta:
		model = Edition
		fields = ['type','date','name','distance']
		widgets = { 
            'type': forms.Select(attrs={'class': 'form-control'}),
            'date': forms.TextInput(attrs={'class': 'form-control'}),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'distance': forms.TextInput(attrs={'class': 'form-control'}),
        }
