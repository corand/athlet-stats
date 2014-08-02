from django import forms
from django.forms import ModelForm
from .models import Race,Edition,RaceType,Modality,SubRace

class RaceForm(ModelForm):
    class Meta:
    	model = Race
    	fields = ['name','month','week']
    	widgets = { 
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'month': forms.Select(attrs={'class': 'form-control'}),
            'week': forms.Select(attrs={'class': 'form-control'}),
        }

class SubRaceForm(ModelForm):
    class Meta:
        model = SubRace
        fields = ['name']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'})
        }

class EditionForm(forms.Form):
    #type = forms.ChoiceField(widget=forms.Select(attrs={'class': 'form-control'}), choices=RaceType.objects.all().values_list('id', 'name'), initial='1')
    #modality = forms.ChoiceField(widget=forms.Select(attrs={'class': 'form-control'}),choices=Modality.objects.all().values_list('id','modality'))
    name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    date = forms.DateTimeField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    distance = forms.IntegerField(widget=forms.TextInput(attrs={'class':'form-control'}),required=False)