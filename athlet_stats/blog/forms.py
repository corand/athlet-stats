from django import forms
from django.forms import ModelForm
from .models import PostEs
from ckeditor.widgets import CKEditorWidget

class PostForm(forms.ModelForm):
    body = forms.CharField(widget=CKEditorWidget())
    class Meta:
        model = PostEs