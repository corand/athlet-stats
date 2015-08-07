# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0006_require_contenttypes_0002'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(null=True, verbose_name='last login', blank=True)),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('email', models.EmailField(unique=True, max_length=255, verbose_name=b'email address', db_index=True)),
                ('profile_picture', models.ImageField(upload_to=b'profiles/', null=True, verbose_name='profile_picture', blank=True)),
                ('name', models.CharField(max_length=30, null=True, verbose_name='name', blank=True)),
                ('first_surname', models.CharField(max_length=30, null=True, verbose_name='first_surname', blank=True)),
                ('second_surname', models.CharField(max_length=30, null=True, verbose_name='second_surname', blank=True)),
                ('gender', models.IntegerField(blank=True, max_length=30, null=True, choices=[(1, b'Hombre'), (2, b'Mujer')])),
                ('self_description_es', models.TextField(null=True, verbose_name='self_description_es', blank=True)),
                ('self_description_eu', models.TextField(null=True, verbose_name='self_description_eu', blank=True)),
                ('coach_description', models.TextField(null=True, verbose_name='coach_description', blank=True)),
                ('date_of_birdth', models.DateField(null=True, blank=True)),
                ('slug', models.SlugField(null=True, blank=True)),
                ('twitter', models.URLField(null=True, blank=True)),
                ('is_active', models.BooleanField(default=True)),
                ('is_admin', models.BooleanField(default=False)),
                ('is_staff', models.BooleanField(default=False)),
                ('groups', models.ManyToManyField(related_query_name='user', related_name='user_set', to='auth.Group', blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(related_query_name='user', related_name='user_set', to='auth.Permission', blank=True, help_text='Specific permissions for this user.', verbose_name='user permissions')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
