# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import migrations

import chat_api.utils.fields


class Migration(migrations.Migration):

    dependencies = [
        ('chat_api', '0008_auto_20170309_0622'),
    ]

    operations = [
        migrations.AddField(
            model_name='survey',
            name='state',
            field=chat_api.utils.fields.JSONField(blank=True, null=True),
        ),
    ]
