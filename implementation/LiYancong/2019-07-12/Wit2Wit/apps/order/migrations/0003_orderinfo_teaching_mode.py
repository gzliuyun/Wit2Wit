# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0002_auto_20190707_2114'),
    ]

    operations = [
        migrations.AddField(
            model_name='orderinfo',
            name='teaching_mode',
            field=models.SmallIntegerField(verbose_name='授业方式', default=1, choices=[(1, '远程教育'), (2, '现场授业')]),
        ),
    ]
