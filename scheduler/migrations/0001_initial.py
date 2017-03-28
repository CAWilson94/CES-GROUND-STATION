# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-03-28 10:24
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AzEl',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('azimuth', models.CharField(max_length=15)),
                ('elevation', models.CharField(max_length=15)),
            ],
        ),
        migrations.CreateModel(
            name='Mission',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=30, unique=True)),
                ('status', models.CharField(max_length=30)),
                ('priority', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='NextPass',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('riseTime', models.DateTimeField()),
                ('setTime', models.DateTimeField()),
                ('duration', models.DurationField()),
                ('maxElevation', models.CharField(max_length=15)),
                ('riseAzimuth', models.CharField(max_length=15)),
                ('setAzimuth', models.CharField(max_length=15)),
                ('mission', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='scheduler.Mission')),
            ],
        ),
        migrations.CreateModel(
            name='TLE',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(default='NAME', max_length=30, unique=True)),
                ('line1', models.CharField(max_length=70)),
                ('line2', models.CharField(max_length=70)),
            ],
        ),
        migrations.AddField(
            model_name='nextpass',
            name='tle',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='scheduler.TLE'),
        ),
        migrations.AddField(
            model_name='mission',
            name='TLE',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='scheduler.TLE'),
        ),
    ]
