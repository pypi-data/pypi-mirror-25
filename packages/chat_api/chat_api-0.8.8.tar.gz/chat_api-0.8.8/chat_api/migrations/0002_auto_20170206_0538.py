# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.conf import settings
from django.db import migrations, models

import chat_api.utils.fields
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('contenttypes', '0002_remove_content_type_name'),
        ('chat_api', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Survey',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('created', models.DateTimeField(db_index=True, auto_now_add=True)),
                ('updated', models.DateTimeField(db_index=True, auto_now=True)),
                ('automated_sender', models.ForeignKey(blank=True, null=True, related_name='automated_surveys_sent_by',
                                                       to=settings.AUTH_USER_MODEL, db_index=False,
                                                       on_delete=django.db.models.deletion.CASCADE)),
            ],
        ),
        migrations.CreateModel(
            name='SurveyAttachment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('description', models.TextField(blank=True)),
                ('object_id', models.PositiveIntegerField(blank=True, null=True)),
                ('options', chat_api.utils.fields.JSONField(blank=True, null=True)),
                ('src', models.FileField(blank=True, null=True, upload_to='')),
                ('thumbnail', chat_api.utils.fields.JSONField(blank=True, null=True)),
                ('title', models.CharField(max_length=255, blank=True)),
                ('type', models.CharField(max_length=50, choices=[('image', 'Image'), ('youtube', 'Youtube'),
                                                                  ('object_reference', 'Object Reference')])),
                ('content_type', models.ForeignKey(null=True, to='contenttypes.ContentType', db_index=False,
                                                   on_delete=django.db.models.deletion.CASCADE)),
            ],
        ),
        migrations.CreateModel(
            name='SurveyItem',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('has_attachments', models.BooleanField(default=False)),
                ('meta', chat_api.utils.fields.JSONField(blank=True, null=True)),
                ('position', models.IntegerField(db_index=True)),
                ('text', models.TextField(blank=True)),
                ('type', models.CharField(max_length=50, default='answer')),
                ('updated', models.DateTimeField(db_index=True, auto_now=True)),
                ('answers', models.ManyToManyField(to='chat_api.Answer')),
                ('related_question', models.ForeignKey(blank=True, null=True, to='chat_api.Question',
                                                       on_delete=django.db.models.deletion.CASCADE)),
                ('sender', models.ForeignKey(blank=True, null=True, to=settings.AUTH_USER_MODEL, db_index=False,
                                             on_delete=django.db.models.deletion.CASCADE)),
                ('survey', models.ForeignKey(to='chat_api.Survey', on_delete=django.db.models.deletion.CASCADE)),
            ],
        ),
        migrations.AlterField(
            model_name='schema',
            name='type',
            field=models.CharField(max_length=100, db_index=True, choices=[('automated_flow', 'Automated Flow')]),
        ),
        migrations.AlterField(
            model_name='thread',
            name='type',
            field=models.CharField(max_length=50, default='consultation',
                                   choices=[('consultation', 'Consultation'), ('triage', 'Triage')]),
        ),
        migrations.AlterField(
            model_name='unreadmessage',
            name='type',
            field=models.CharField(max_length=50, blank=True, db_index=True, default='consultation',
                                   choices=[('consultation', 'Consultation'), ('triage', 'Triage')]),
        ),
        migrations.AlterField(
            model_name='userthread',
            name='type',
            field=models.CharField(max_length=50, db_index=True, editable=False,
                                   choices=[('consultation', 'Consultation'), ('triage', 'Triage')]),
        ),
        migrations.AddField(
            model_name='surveyattachment',
            name='item',
            field=models.ForeignKey(to='chat_api.SurveyItem', on_delete=django.db.models.deletion.CASCADE),
        ),
        migrations.AddField(
            model_name='survey',
            name='schema',
            field=models.ForeignKey(blank=True, null=True, to='chat_api.Schema', db_index=False,
                                    on_delete=django.db.models.deletion.CASCADE),
        ),
        migrations.AddField(
            model_name='survey',
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=django.db.models.deletion.CASCADE),
        ),
    ]
