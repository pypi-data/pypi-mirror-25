# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('coop_cms', '0013_auto_20170607_1508'),
    ]

    operations = [
        migrations.AlterField(
            model_name='articlecategory',
            name='sites',
            field=models.ManyToManyField(default=[18], to='sites.Site', verbose_name='site'),
        ),
        migrations.AlterField(
            model_name='newsletter',
            name='site',
            field=models.ForeignKey(default=18, verbose_name='site', to='sites.Site'),
        ),
    ]
