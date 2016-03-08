# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Adminstrator',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('a_id', models.CharField(max_length=20)),
                ('mail', models.CharField(max_length=20)),
                ('phone', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('s_id', models.CharField(max_length=20)),
                ('pwd', models.CharField(max_length=20)),
                ('s_name', models.CharField(max_length=20)),
                ('college', models.CharField(max_length=20)),
                ('mail', models.CharField(max_length=20)),
                ('phone', models.CharField(max_length=20)),
                ('grade', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Teacher',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('t_id', models.CharField(max_length=20)),
                ('pwd', models.CharField(max_length=20)),
                ('t_name', models.CharField(max_length=20)),
                ('college', models.CharField(max_length=20)),
                ('mail', models.CharField(max_length=20)),
                ('phone', models.CharField(max_length=20)),
                ('title', models.CharField(max_length=10)),
            ],
        ),
    ]
