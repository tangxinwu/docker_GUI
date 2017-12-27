# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-12-04 00:46
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ImagePull',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ImageName', models.CharField(max_length=50, verbose_name='镜像名')),
                ('PullStatus', models.SmallIntegerField(choices=[(0, '下载进行中'), (1, '下载已经完成')], verbose_name='下载状态')),
            ],
        ),
    ]
