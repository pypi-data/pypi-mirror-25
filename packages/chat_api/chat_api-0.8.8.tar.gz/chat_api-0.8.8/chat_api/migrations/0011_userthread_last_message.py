# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import migrations, models

import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('chat_api', '0010_auto_20170313_0919'),
    ]

    operations = [
        migrations.AddField(
            model_name='userthread',
            name='last_message',
            field=models.ForeignKey(blank=True, null=True, related_name='last_in_user_threads', to='chat_api.Message',
                                    db_index=False, on_delete=django.db.models.deletion.CASCADE),
        ),
    ]
