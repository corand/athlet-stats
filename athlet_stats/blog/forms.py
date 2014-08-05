from django import forms
from django.forms import ModelForm
from .models import Post
from ckeditor.widgets import CKEditorWidget


STATUS_CHOICES = (
    (1, 'Borrador'),
    (2, 'Publicado'),
    (3, 'Publicado en privado')
)


class PostForm(ModelForm):
	status = forms.ChoiceField(widget=forms.Select(attrs={'class':'form-control'}),choices=STATUS_CHOICES)
	class Meta:
		model = Post
		fields = ['title_es','title_eu','body_es','body_eu','status']
		widgets = { 
            'title_es': forms.TextInput(attrs={'class': 'form-control','placeholder': 'Titulo del post'}),
            'title_eu': forms.TextInput(attrs={'class': 'form-control','placeholder': 'Postaren izenburua'}),
            'body_es': forms.CharField(widget=CKEditorWidget()),
            'body_eu': forms.CharField(widget=CKEditorWidget()),
        }