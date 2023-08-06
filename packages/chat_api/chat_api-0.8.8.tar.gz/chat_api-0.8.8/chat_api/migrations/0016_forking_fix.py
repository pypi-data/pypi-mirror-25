# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat_api', '0015_forking'),
    ]

    operations = [
        migrations.AddField(
            model_name='variablemodification',
            name='related_message_answer_id',
            field=models.IntegerField(null=True, blank=True),
        ),
    ]
