# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('goods', '0001_initial'),
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='goodsstore',
            name='teacher',
            field=models.ForeignKey(verbose_name='所属教师', to='user.Teacher'),
        ),
        migrations.AddField(
            model_name='goodssku',
            name='goods',
            field=models.ForeignKey(verbose_name='商品SPU', to='goods.Goods'),
        ),
        migrations.AddField(
            model_name='goodssku',
            name='type',
            field=models.ForeignKey(verbose_name='商品种类', to='goods.GoodsType'),
        ),
        migrations.AddField(
            model_name='goodsimage',
            name='sku',
            field=models.ForeignKey(verbose_name='商品', to='goods.GoodsSKU'),
        ),
        migrations.AddField(
            model_name='goods',
            name='store',
            field=models.ForeignKey(verbose_name='所属商店', to='goods.GoodsStore'),
        ),
    ]
