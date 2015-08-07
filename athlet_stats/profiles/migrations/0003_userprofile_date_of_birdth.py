# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0002_remove_userprofile_date_of_birdth'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='date_of_birdth',
            field=models.DateField(null=True, blank=True),
        ),
    ]
