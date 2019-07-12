# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='addr',
            field=models.CharField(verbose_name='地址', max_length=50, default=''),
        ),
        migrations.AddField(
            model_name='user',
            name='birthday',
            field=models.DateField(verbose_name='生日', blank=True, null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='image',
            field=models.ImageField(verbose_name='用户头像', default='', upload_to='users/%Y/%m'),
        ),
        migrations.AddField(
            model_name='user',
            name='mobile',
            field=models.CharField(verbose_name='手机', max_length=11, default=''),
        ),
        migrations.AddField(
            model_name='user',
            name='nick_name',
            field=models.CharField(verbose_name='昵称', max_length=50, default=''),
        ),
    ]
