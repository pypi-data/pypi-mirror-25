# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import migrations, models

import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('chat_api', '0002_auto_20170206_0538'),
    ]

    operations = [
        migrations.AlterField(
            model_name='attachment',
            name='message',
            field=models.ForeignKey(related_name='attachments', to='chat_api.Message',
                                    on_delete=django.db.models.deletion.CASCADE),
        ),
    ]
