# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import migrations, models

import chat_api.utils.fields


class Migration(migrations.Migration):

    dependencies = [
        ('chat_api', '0014_auto_20170523_0812'),
    ]

    operations = [
        migrations.AddField(
            model_name='question',
            name='variable_modifications',
            field=chat_api.utils.fields.JSONField(blank=True, default=list),
        ),
        migrations.AddField(
            model_name='question',
            name='forking_rules',
            field=chat_api.utils.fields.JSONField(blank=True, default=list),
        ),
        migrations.AddField(
            model_name='question',
            name='show_as_type',
            field=models.CharField(max_length=50, default="automated_message"),
        ),
        migrations.AddField(
            model_name='answer',
            name='variable_modifications',
            field=chat_api.utils.fields.JSONField(blank=True, default=list),
        ),
        migrations.AddField(
            model_name='answer',
            name='exclusive',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='userthread',
            name='variables_pool',
            field=chat_api.utils.fields.JSONField(blank=True, default=dict),
        ),
        migrations.CreateModel(
            name='VariableModification',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('variable_modifications', chat_api.utils.fields.JSONField(blank=True, default=list)),
                ('user_thread', models.ForeignKey("chat_api.UserThread", related_name="variable_modifications",
                                                  on_delete=models.CASCADE)),
                ('related_message', models.ForeignKey("chat_api.Message", on_delete=models.CASCADE, null=True,
                                                      blank=True)),
            ],
        ),
    ]
