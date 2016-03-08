# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0001_initial'),
        ('chenge', '0002_auto_20151121_1501'),
    ]

    operations = [
        migrations.CreateModel(
            name='Userprofile',
            fields=[
                ('user', models.OneToOneField(primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('file', models.FileField(upload_to=b'./data/')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
