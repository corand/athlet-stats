# -*- encoding: utf-8 -*-
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from durationfield.db.models.fields.duration import DurationField
from django.contrib.auth import get_user_model as user_model
from datetime import date
from snippets.slughifi import slughifi
from django.conf import settings
#User = user_model()



MONTH_CHOICES = (
    (1, 'Enero'),
    (2, 'Febrero'),
    (3, 'Marzo'),
    (4, 'Abril'),
    (5, 'Mayo'),
    (6, 'Junio'),
    (7, 'Julio'),
    (8, 'Agosto'),
    (9, 'Septiembre'),
    (10, 'Octubre'),
    (11, 'Noviembre'),
    (12, 'Diciembre')
)

WEEK_CHOICES = (
    (1,'Uno'),
    (2,'Dos'),
    (3,'Tres'),
    (4,'Cuatro'),
)

class Season(models.Model):
    name = models.SlugField(max_length=100)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    def save(self,*args,**kwargs):
        self.name = slughifi(self.name)
        super(Season, self).save(*args, **kwargs)

    def __unicode__(self):
        return str(self.id) + self.name


class Race(models.Model):
    name = models.CharField(max_length=100,verbose_name="Nombre",help_text="Nombre genérico de la competición")
    month = models.PositiveIntegerField(choices=MONTH_CHOICES,verbose_name="Mes",help_text="Mes en el que se disputa típicamente") # mes en el que se disputa tipicamente la carrera
    week = models.PositiveIntegerField(choices=WEEK_CHOICES,verbose_name="Semana",help_text="Orden aproximado de la semana en la que se disputa la competición") # semana en la que se disputa tipicamente la carrera
    creator = models.ForeignKey(settings.AUTH_USER_MODEL)

    def __unicode__(self):
        return self.name

class RaceType(models.Model):
    name = models.CharField(max_length=100) # pista indoor, pista outdoor,road,mointain,other

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
    order = models.PositiveIntegerField()

    def __unicode__(self):
        return self.race_type.name + " - " + self.modality

class SubRace(models.Model):
    name = models.CharField(max_length=100)
    race = models.ForeignKey(Race)

    def __unicode__(self):
        return self.race.name + ' - ' + self.name

class Edition(models.Model):
    type = models.ForeignKey(Modality)
    date = models.DateTimeField()
    race = models.ForeignKey(Race)
    name = models.CharField(max_length=100)
    distance = models.PositiveIntegerField(blank=True,null=True)
    subRace = models.ForeignKey(SubRace,blank=True,null=True)
    creator = models.ForeignKey(settings.AUTH_USER_MODEL)

    def is_past(self):
        if timezone.now() > self.date:
            return True
        return False

    def __unicode__(self):
        return self.name

class Objective(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    edition = models.ForeignKey(Edition)
    timemark = DurationField(blank=True,null=True)
    distancemark = models.PositiveIntegerField(blank=True,null=True)
    position = models.PositiveIntegerField(blank=True,null=True)
    position_cat = models.PositiveIntegerField(blank=True,null=True)
    duda = models.BooleanField(default=False)
    comment = models.TextField(blank=True,null=True)

    @property
    def is_past_due(self):
        if date.today() > self.edition.date:
            return True
        return False

    def __unicode__(self):
        return self.edition.name + " - " + self.user.name


class Result(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    edition = models.ForeignKey(Edition)
    timemark = DurationField(blank=True,null=True)
    distancemark = models.FloatField(blank=True,null=True)
    position = models.PositiveIntegerField(blank=True,null=True)
    position_cat = models.PositiveIntegerField(blank=True,null=True)
    comment = models.TextField(blank=True,null=True)

    class Meta:
        managed = True

    def __unicode__(self):
        return self.edition.name + " - " + self.user.name