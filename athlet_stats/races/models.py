from django.db import models
from durationfield.db.models.fields.duration import DurationField
from django.contrib.auth.models import User

class Race(models.Model):
	name = models.CharField(max_length=100)
	month = models.PositiveIntegerField() # mes en el que se disputa tipicamente la carrera
	week = models.PositiveIntegerField() # semana en la que se disputa tipicamente la carrera

	def __unicode__(self):
		return self.name

class RaceType(models.Model):
	name = models.CharField(max_length=100) # indoor,outdoor,road,mointain,other

	def __unicode__(self):
		return self.name


class ResultType(models.Model):
	name = models.CharField(max_length=100) # resultado en metros, tiempo

	def __unicode__(self):
		return self.name


class Modality(models.Model):
	race_type = models.ForeignKey(RaceType)
	result_type = models.ForeignKey(ResultType)
	modality = models.CharField(max_length=100)
	distance = models.PositiveIntegerField(blank=True,null=True)

	def __unicode__(self):
		return str(self.race_type) + " - " + self.modality 

class Edition(models.Model):
	type = models.ForeignKey(Modality)
	date = models.DateTimeField()
	race = models.ForeignKey(Race)
	name = models.CharField(max_length=100)
	distance = models.PositiveIntegerField(blank=True,null=True)

	def __unicode__(self):
		return self.name

class Objective(models.Model):
	user = models.ForeignKey(User)
	edition = models.ForeignKey(Edition)
	timemark = DurationField(blank=True,null=True)
	distancemark = models.PositiveIntegerField(blank=True,null=True)
	position = models.PositiveIntegerField(blank=True,null=True)
	comment = models.TextField(blank=True,null=True)

	def __unicode__(self):
		return self.edition.name + " - " + self.user.username


class Result(models.Model):
	user = models.ForeignKey(User)
	edition = models.ForeignKey(Edition)
	timemark = DurationField(blank=True,null=True)
	distancemark = models.PositiveIntegerField(blank=True,null=True)
	position = models.PositiveIntegerField(blank=True,null=True)
	comment = models.TextField()

	def __unicode__(self):
		return self.edition.name + " - " + self.user.username