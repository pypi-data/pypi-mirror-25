# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import filer.fields.image


class Migration(migrations.Migration):

    dependencies = [
        ('djangocms_page_image', '0002_auto_20150124_0925'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='imageextension',
            options={'verbose_name': 'page image and teaser'},
        ),
        migrations.AddField(
            model_name='imageextension',
            name='teaser',
            field=models.TextField(verbose_name='teaser', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='imageextension',
            name='image',
            field=filer.fields.image.FilerImageField(verbose_name='image', blank=True, to='filer.Image'),
            preserve_default=True,
        ),
    ]
