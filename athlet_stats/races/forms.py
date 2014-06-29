from django import forms
from django.forms import ModelForm
from .models import Race,Edition,RaceType,Modality

class RaceForm(ModelForm):
    class Meta:
    	model = Race
    	fields = ['name','month','week']
    	widgets = { 
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'month': forms.Select(attrs={'class': 'form-control'}),
            'week': forms.Select(attrs={'class': 'form-control'}),
        }



class RaceTypeForm(forms.Form):
	type = forms.ChoiceField(widget=forms.Select(attrs={'class': 'form-control'}), choices=RaceType.objects.all().values_list('id', 'name'), initial='1')


class EditionForm(forms.Form):
	modality = forms.ChoiceField(widget=forms.Select(attrs={'class': 'form-control'}), choices=Modality.objects.filter(race_type=1).values_list('id','modality'), initial='2')
	date = forms.DateTimeField(widget=forms.TextInput(attrs={'class': 'form-control'}))
	name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
	distance = forms.IntegerField(widget=forms.TextInput(attrs={'class':'form-control'}))