# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0002_auto_20190708_0954'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='user_type',
            field=models.SmallIntegerField(verbose_name='用户类型', default=1, choices=[(1, '学习者'), (2, '授业者'), (3, '管理员')]),
        ),
    ]
