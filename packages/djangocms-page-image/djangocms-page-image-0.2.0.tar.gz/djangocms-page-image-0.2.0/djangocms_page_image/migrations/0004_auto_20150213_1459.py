# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
from django.utils.translation import ugettext_lazy as _

import filer

STYLE_CHOICES = [
    (x, _(y))
    for x, y
    in getattr(settings, 'DJANGOCMS_PAGE_IMAGE_CPP_STYLE_CHOICES', [])
]
DEFAULT_STYLE = getattr(
    settings,
    'DJANGOCMS_PAGE_IMAGE_CPP_DEFAULT_STYLE',
    ''
)

class Migration(migrations.Migration):

    dependencies = [
        ('djangocms_page_image', '0003_auto_20150125_2116'),
    ]

    operations = [
        migrations.AddField(
            model_name='childpagepreviewplugin',
            name='style',
            field=models.CharField(
                max_length=50,
                verbose_name='style',
                blank=True,
                choices=STYLE_CHOICES,
                default=DEFAULT_STYLE
            ),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='imageextension',
            name='show_preview',
            field=models.BooleanField(default=True, verbose_name='show preview?'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='imageextension',
            name='image',
            field=filer.fields.image.FilerImageField(verbose_name='image', blank=True, to='filer.Image', null=True),
            preserve_default=True,
        ),
    ]
