from django.db import models
from ckeditor.fields import RichTextField
from django.contrib.auth.models import User

# Create your models here.

class Post(models.Model):
	created = models.DateTimeField(auto_now_add=True)
	author = models.ForeignKey(User)
	status = models.CharField(max_length=100)
	
	def __unicode__(self):
		return str(self.id)


class PostEs(models.Model):
	title = models.CharField(max_length=100)
	body = RichTextField()
	post = models.ForeignKey(Post)

	def __unicode__(self):
		return self.title

class PostEus(models.Model):
	title = models.CharField(max_length=100)
	body = RichTextField()
	post = models.ForeignKey(Post)

	def __unicode__(self):
		return self.title
