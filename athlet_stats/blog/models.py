from django.db import models
from ckeditor.fields import RichTextField
from django.contrib.auth.models import User
from snippets.random_primary import RandomPrimaryIdModel
from django.contrib.auth import get_user_model as user_model
from snippets.slughifi import slughifi
User = user_model()

# Create your models here.

class Post(RandomPrimaryIdModel):
	created = models.DateTimeField(auto_now_add=True)
	title_es = models.CharField(max_length=100)
	body_es = RichTextField(blank=True,null=True)
	title_eu = models.CharField(max_length=100)
	body_eu = RichTextField(blank=True,null=True)
	slug_es = models.SlugField(max_length=100)
	slug_eu = models.SlugField(max_length=100)
	author = models.ForeignKey(User)
	status = models.CharField(max_length=100)

	def save(self,*args,**kwargs):
		self.slug_es = slughifi(self.title_es)
		self.slug_eu = slughifi(self.title_eu)
		super(Post, self).save(*args, **kwargs)

	def __unicode__(self):
		return str(self.id) + self.title_es