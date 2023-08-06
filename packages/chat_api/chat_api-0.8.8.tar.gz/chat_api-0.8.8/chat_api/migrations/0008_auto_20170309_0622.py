# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import migrations, models

import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('chat_api', '0007_auto_20170303_1657'),
    ]

    operations = [
        migrations.AlterField(
            model_name='attachmenttemplate',
            name='question',
            field=models.ForeignKey(blank=True, null=True, related_name='attachments', to='chat_api.Question',
                                    on_delete=django.db.models.deletion.CASCADE),
        ),
        migrations.AlterField(
            model_name='surveyitem',
            name='answers',
            field=models.ManyToManyField(blank=True, to='chat_api.Answer'),
        ),
        migrations.AlterUniqueTogether(
            name='question',
            unique_together=set([('qid', 'schema'), ('position', 'schema')]),
        ),
    ]
