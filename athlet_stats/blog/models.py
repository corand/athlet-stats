from django.db import models
from ckeditor.fields import RichTextField
from django.contrib.auth.models import User

# Create your models here.
class Post(models.Model):
	title = models.CharField(max_length=100)
	body = RichTextField()
	created = models.DateTimeField(auto_now_add=True)
	author = models.ForeignKey(User)

	def __unicode__(self):
		return self.title