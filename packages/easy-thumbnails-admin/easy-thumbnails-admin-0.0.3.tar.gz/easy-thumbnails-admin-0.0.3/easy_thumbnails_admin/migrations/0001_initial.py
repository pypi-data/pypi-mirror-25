# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import jsonfield.fields


class Migration(migrations.Migration):

    dependencies = [
        ('easy_thumbnails', '0002_thumbnaildimensions'),
    ]

    operations = [
        migrations.CreateModel(
            name='ThumbnailOption',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('alias', models.CharField(max_length=42)),
                ('options', jsonfield.fields.JSONField(null=True, blank=True)),
                ('source', models.ForeignKey(related_name='options', to='easy_thumbnails.Source')),
            ],
        ),
        migrations.AlterUniqueTogether(
            name='thumbnailoption',
            unique_together=set([('source', 'alias')]),
        ),
    ]
