from django.db import models

class Race(models.Model):
	name = models.CharField(max_length=100)

	def __unicode__(self):
		return self.name


class Type(models.Model):
	type = models.CharField(max_length=100) # indoor,outdoor,road,mointain,other
	name = models.CharField(max_length=100)
	distance = models.PositiveIntegerField(blank=True,null=True)

	def __unicode__(self):
		return self.name

class Edition(models.Model):
	date = models.DateTimeField()
	race = models.ForeignKey(Race)
	name = models.CharField(max_length=100)
	type = models.ForeignKey(Type)
	distance = models.PositiveIntegerField(blank=True,null=True)

	def __unicode__(self):
		return self.name