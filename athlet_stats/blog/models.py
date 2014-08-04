from django.db import models
from ckeditor.fields import RichTextField
from django.contrib.auth.models import User

# Create your models here.

class Post(models.Model):
	created = models.DateTimeField(auto_now_add=True)
	title_es = models.CharField(max_length=100)
	body_es = RichTextField()
	title_eu = models.CharField(max_length=100)
	body_eu = RichTextField()
	author = models.ForeignKey(User)
	status = models.CharField(max_length=100)
	
	def __unicode__(self):
		return str(self.id) + self.title_es