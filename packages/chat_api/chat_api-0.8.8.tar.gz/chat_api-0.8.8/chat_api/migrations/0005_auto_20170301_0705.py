# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.conf import settings
from django.db import migrations, models

import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('chat_api', '0004_message_predecessor'),
    ]

    operations = [
        migrations.CreateModel(
            name='ThreadWSSubscription',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('thread', models.ForeignKey(related_name='ws_subscription', to='chat_api.Thread',
                                             on_delete=django.db.models.deletion.CASCADE)),
                ('user', models.ForeignKey(unique=True, related_name='ws_subscription', to=settings.AUTH_USER_MODEL,
                                           on_delete=django.db.models.deletion.CASCADE)),
            ],
        ),
        migrations.AlterField(
            model_name='question',
            name='type',
            field=models.CharField(max_length=50, choices=[('choice', 'Choice'), ('multichoice', 'Multichoice'),
                                                           ('text', 'Text'), ('date', 'Date'), ('bool', 'Bool'),
                                                           ('int', 'Int'), ('float', 'Float'), ('range', 'Range'),
                                                           ('message', 'Message (no answers)')]),
        ),
    ]
