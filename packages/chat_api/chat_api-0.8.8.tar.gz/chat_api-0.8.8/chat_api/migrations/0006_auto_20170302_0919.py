# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.conf import settings
from django.db import migrations, models

import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('chat_api', '0005_auto_20170301_0705'),
    ]

    operations = [
        migrations.RenameField(
            model_name='attachment',
            old_name='src',
            new_name='file',
        ),
        migrations.RenameField(
            model_name='attachmenttemplate',
            old_name='src',
            new_name='file',
        ),
        migrations.RenameField(
            model_name='surveyattachment',
            old_name='src',
            new_name='file',
        ),
        migrations.AddField(
            model_name='attachment',
            name='url',
            field=models.URLField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='attachmenttemplate',
            name='url',
            field=models.URLField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='surveyattachment',
            name='url',
            field=models.URLField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='threadwssubscription',
            name='user',
            field=models.OneToOneField(related_name='ws_subscription', to=settings.AUTH_USER_MODEL,
                                       on_delete=django.db.models.deletion.CASCADE),
        ),
    ]
