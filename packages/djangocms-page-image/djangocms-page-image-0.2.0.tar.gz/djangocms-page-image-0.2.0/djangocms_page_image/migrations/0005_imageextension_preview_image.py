# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import filer.fields.image


class Migration(migrations.Migration):

    dependencies = [
        ('filer', '0001_initial'),
        ('djangocms_page_image', '0004_auto_20150213_1459'),
    ]

    operations = [
        migrations.AddField(
            model_name='imageextension',
            name='preview_image',
            field=filer.fields.image.FilerImageField(related_name='preview_image_extensions', blank=True, to='filer.Image', help_text='leave blank to use page image', null=True, verbose_name='preview image'),
            preserve_default=True,
        ),
    ]
