from django.db import models
from django.contrib.auth.models import User

class Race(models.Model):
	name = models.CharField(max_length=100)

	def __unicode__(self):
		return self.name


class Type(models.Model):
	type = models.CharField(max_length=100) # indoor,outdoor,road,mointain,other
	name = models.CharField(max_length=100)
	distance = models.PositiveIntegerField(blank=True,null=True)

	def __unicode__(self):
		return self.type + " - " + self.name 

class Edition(models.Model):
	date = models.DateTimeField()
	race = models.ForeignKey(Race)
	name = models.CharField(max_length=100)
	type = models.ForeignKey(Type)
	distance = models.PositiveIntegerField(blank=True,null=True)

	def __unicode__(self):
		return self.name

class Objective(models.Model):
	user = models.ForeignKey(User)
	edition = models.ForeignKey(Edition)
	mark = models.TimeField()
	position = models.PositiveIntegerField()
	comment = models.TextField()

	def __unicode__(self):
		return self.edition.name + " - " + self.user.username


class Result(models.Model):
	user = models.ForeignKey(User)
	edition = models.ForeignKey(Edition)
	mark = models.TimeField()
	position = models.PositiveIntegerField()
	comment = models.TextField()

	def __unicode__(self):
		return self.edition.name + " - " + self.user.username