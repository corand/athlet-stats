from django import forms
from django.forms import ModelForm
from .models import PostEs
from ckeditor.widgets import CKEditorWidget


STATUS_CHOICES = (
    (1, 'Borrador'),
    (2, 'Publicado'),
    (3, 'Publicado en privado')
)


class PostForm(forms.Form):
	title_es = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','placeholder': 'Titulo del post'}))
	title_eu = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','placeholder': 'Postaren izenburua'}))
	body_es = forms.CharField(widget=CKEditorWidget())
	body_eu = forms.CharField(widget=CKEditorWidget())
	status = forms.ChoiceField(widget=forms.Select(attrs={'class':'form-control'}),choices=STATUS_CHOICES)