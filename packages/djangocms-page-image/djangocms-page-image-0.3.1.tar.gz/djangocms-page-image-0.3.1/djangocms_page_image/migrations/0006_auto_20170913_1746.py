# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('djangocms_page_image', '0005_imageextension_preview_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='imageextension',
            name='extra_classes',
            field=models.CharField(max_length=512, verbose_name='extra classes', blank=True),
        ),
        migrations.AlterField(
            model_name='childpagepreviewplugin',
            name='cmsplugin_ptr',
            field=models.OneToOneField(parent_link=True, related_name='djangocms_page_image_childpagepreviewplugin', auto_created=True, primary_key=True, serialize=False, to='cms.CMSPlugin'),
        ),
    ]
