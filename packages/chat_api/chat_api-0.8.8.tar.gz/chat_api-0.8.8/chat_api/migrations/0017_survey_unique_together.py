# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("chat_api", "0016_forking_fix"),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='surveyitem',
            unique_together=set([("related_question", "survey")]),
        ),
    ]
