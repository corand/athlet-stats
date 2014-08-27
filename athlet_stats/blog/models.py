from django.db import models
from ckeditor.fields import RichTextField
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model as user_model
User = user_model()

# Create your models here.

class Post(models.Model):
	created = models.DateTimeField(auto_now_add=True)
	title_es = models.CharField(max_length=100)
	body_es = RichTextField(blank=True,null=True)
	title_eu = models.CharField(max_length=100)
	body_eu = RichTextField(blank=True,null=True)
#	slug_es
#	slug_eu
	author = models.ForeignKey(User)
	status = models.CharField(max_length=100)
	
	def __unicode__(self):
		return str(self.id) + self.title_es