# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cms', '0016_auto_20160608_1535'),
        ('djangocms_page_image', '0006_auto_20170913_1746'),
    ]

    operations = [
        migrations.CreateModel(
            name='SiblingPagePreviewPlugin',
            fields=[
                ('cmsplugin_ptr', models.OneToOneField(parent_link=True, related_name='djangocms_page_image_siblingpagepreviewplugin', auto_created=True, primary_key=True, serialize=False, to='cms.CMSPlugin')),
                ('style', models.CharField(default=b'', max_length=50, verbose_name='style', blank=True)),
            ],
            options={
                'abstract': False,
            },
            bases=('cms.cmsplugin',),
        ),
        migrations.AlterModelOptions(
            name='imageextension',
            options={'verbose_name': 'Page Image and Teaser'},
        ),
    ]
