# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat_api', '0009_survey_fields_visibility'),
    ]

    operations = [
        migrations.AlterField(
            model_name='message',
            name='type',
            field=models.CharField(max_length=50, db_index=True, default='message'),
        ),
    ]
