# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import filer.fields.image


class Migration(migrations.Migration):

    dependencies = [
        ('cms', '0003_auto_20140926_2347'),
        ('filer', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ImageExtension',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('extended_object', models.OneToOneField(editable=False, to='cms.Page')),
                ('image', filer.fields.image.FilerImageField(verbose_name='image', to='filer.Image')),
                ('public_extension', models.OneToOneField(related_name='draft_extension', null=True, editable=False, to='djangocms_page_image.ImageExtension')),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
    ]
