# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import migrations, models

import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('chat_api', '0003_auto_20170227_1037'),
    ]

    operations = [
        migrations.AddField(
            model_name='message',
            name='predecessor',
            field=models.ForeignKey(blank=True, null=True, related_name='preceeding_messages', to='chat_api.Question',
                                    on_delete=django.db.models.deletion.CASCADE),
        ),
    ]
