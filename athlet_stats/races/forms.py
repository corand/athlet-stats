from django import forms
from django.forms import ModelForm
from .models import Race,Edition,RaceType,Modality,SubRace,Result


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



class ObjectiveForm(forms.Form):
    horas = forms.IntegerField(widget=forms.TextInput(attrs={'class':'form-control duration','placeholder': 'HH'}),required=False)
    minutos = forms.IntegerField(widget=forms.TextInput(attrs={'class':'form-control duration','placeholder': 'MM'}),required=False)
    segundos = forms.IntegerField(widget=forms.TextInput(attrs={'class':'form-control duration','placeholder': 'SS'}),required=False)
    centesimas = forms.IntegerField(widget=forms.TextInput(attrs={'class':'form-control duration','placeholder': 'CC'}),required=False)
    distancia = forms.FloatField(widget=forms.TextInput(attrs={'class':'form-control duration'}),required=False)
    puesto = forms.IntegerField(widget=forms.TextInput(attrs={'class':'form-control duration'}),required=False)
    puesto_cat = forms.IntegerField(widget=forms.TextInput(attrs={'class':'form-control duration'}),required=False)
    comentarios = forms.CharField(widget=forms.Textarea(attrs={'class':'form-control','placeholder': 'Cuentanos un poco la idea con la que vas a acudir'}),required=False)


class ResultForm(forms.Form):
    horas = forms.IntegerField(widget=forms.TextInput(attrs={'class':'form-control duration','placeholder': 'HH'}),required=False)
    minutos = forms.IntegerField(widget=forms.TextInput(attrs={'class':'form-control duration','placeholder': 'MM'}),required=False)
    segundos = forms.IntegerField(widget=forms.TextInput(attrs={'class':'form-control duration','placeholder': 'SS'}),required=False)
    centesimas = forms.IntegerField(widget=forms.TextInput(attrs={'class':'form-control duration','placeholder': 'CC'}),required=False)
    distancia = forms.FloatField(widget=forms.TextInput(attrs={'class':'form-control duration'}),required=False)
    puesto = forms.IntegerField(widget=forms.TextInput(attrs={'class':'form-control duration'}),required=False)
    puesto_cat = forms.IntegerField(widget=forms.TextInput(attrs={'class':'form-control duration'}),required=False)
    comentarios = forms.CharField(widget=forms.Textarea(attrs={'class':'form-control','placeholder': 'Cuentanos un poco tu prueba'}),required=False)


class EditionForm(forms.Form):
    TYPE_CHOICES = [('', '-- Selecciona un tipo de carrera --'), ] + [(t.id, t.name) for t in RaceType.objects.all()]
    MODALITY_CHOICES = [(c.id, c.modality) for c in Modality.objects.all()]
    MODALITY_CHOICES.insert(0, ('', '-- Seleccionar tipo de carrera primero --'))
    type = forms.ChoiceField(widget=forms.Select(attrs={'class': 'form-control'}), choices=TYPE_CHOICES)
    modality = forms.ChoiceField(widget=forms.Select(attrs={'class': 'form-control'}),choices=MODALITY_CHOICES)
    name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    date = forms.DateTimeField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    distance = forms.IntegerField(widget=forms.TextInput(attrs={'class':'form-control'}),required=False)