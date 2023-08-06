# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat_api', '0006_auto_20170302_0919'),
    ]

    operations = [
        migrations.AddField(
            model_name='attachment',
            name='thumbnail_image',
            field=models.ImageField(blank=True, null=True, upload_to=''),
        ),
        migrations.AddField(
            model_name='attachmenttemplate',
            name='thumbnail_image',
            field=models.ImageField(blank=True, null=True, upload_to=''),
        ),
        migrations.AddField(
            model_name='surveyattachment',
            name='thumbnail_image',
            field=models.ImageField(blank=True, null=True, upload_to=''),
        ),
    ]
