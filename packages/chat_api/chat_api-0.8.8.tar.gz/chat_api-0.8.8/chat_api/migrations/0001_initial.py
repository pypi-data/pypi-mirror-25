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
    ]

    operations = [
        migrations.CreateModel(
            name='Answer',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('meta', chat_api.utils.fields.JSONField(blank=True, null=True)),
                ('next_qid', models.IntegerField()),
                ('position', models.IntegerField(db_index=True)),
                ('text', models.TextField()),
            ],
            options={
                'ordering': ('position',),
            },
        ),
        migrations.CreateModel(
            name='Attachment',
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
            name='AttachmentTemplate',
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
            name='Group',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('name', models.CharField(max_length=100, db_index=True)),
                ('position', models.IntegerField(db_index=True)),
            ],
            options={
                'ordering': ('position',),
            },
        ),
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('deleted', models.BooleanField(default=False)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('has_attachments', models.BooleanField(default=False)),
                ('meta', chat_api.utils.fields.JSONField(blank=True, null=True)),
                ('text', models.TextField(blank=True)),
                ('type', models.CharField(max_length=50, default='message')),
                ('updated', models.DateTimeField(db_index=True, auto_now=True)),
                ('answers', models.ManyToManyField(blank=True, to='chat_api.Answer')),
            ],
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('choice_open', models.BooleanField(default=False)),
                ('has_attachments', models.BooleanField(default=False)),
                ('meta', chat_api.utils.fields.JSONField(blank=True, null=True)),
                ('next_qid', models.IntegerField(blank=True, null=True)),
                ('position', models.IntegerField(db_index=True)),
                ('qid', models.IntegerField(db_index=True)),
                ('range_from', models.FloatField(blank=True, null=True)),
                ('range_to', models.FloatField(blank=True, null=True)),
                ('required', models.BooleanField(default=False)),
                ('text', models.TextField()),
                ('type', models.CharField(max_length=50, choices=[
                    ('choice', 'Choice'), ('multichoice', 'Multichoice'), ('text', 'Text'), ('date', 'Date'),
                    ('bool', 'Bool'), ('int', 'Int'), ('float', 'Float'), ('range', 'Range')])),
                ('group', models.ForeignKey(blank=True, null=True, related_name='questions', to='chat_api.Group',
                                            on_delete=django.db.models.deletion.CASCADE)),
            ],
            options={
                'ordering': ('position',),
            },
        ),
        migrations.CreateModel(
            name='Schema',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('deprecated', models.BooleanField(db_index=True, default=False)),
                ('name', models.CharField(max_length=100)),
                ('published', models.BooleanField(db_index=True, default=False)),
                ('type', models.CharField(max_length=100, db_index=True, choices=[
                    ('survey', 'Survey'), ('automated_flow', 'Automated Flow')])),
                ('version', models.IntegerField(default=1)),
            ],
        ),
        migrations.CreateModel(
            name='Thread',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('title', models.CharField(max_length=255, blank=True)),
                ('type', models.CharField(max_length=50, default='chat', choices=[
                    ('chat', 'Chat'), ('survey', 'Survey'), ('tracker', 'Tracker')])),
                ('updated', models.DateTimeField(auto_now=True)),
                ('last_message', models.ForeignKey(blank=True, null=True, related_name='last_in_threads',
                                                   to='chat_api.Message', db_index=False,
                                                   on_delete=django.db.models.deletion.CASCADE)),
            ],
        ),
        migrations.CreateModel(
            name='UnreadMessage',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('type', models.CharField(max_length=50, blank=True, db_index=True, default='chat', choices=[
                    ('chat', 'Chat'), ('survey', 'Survey'), ('tracker', 'Tracker')])),
                ('message', models.ForeignKey(related_name='unread_states', to='chat_api.Message',
                                              on_delete=django.db.models.deletion.CASCADE)),
                ('thread', models.ForeignKey(related_name='unread_messages', to='chat_api.Thread',
                                             on_delete=django.db.models.deletion.CASCADE)),
                ('user', models.ForeignKey(related_name='unread_messages', to=settings.AUTH_USER_MODEL,
                                           on_delete=django.db.models.deletion.CASCADE)),
            ],
        ),
        migrations.CreateModel(
            name='UserThread',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('created', models.DateTimeField(db_index=True)),
                ('frequency_unit', models.CharField(max_length=50, blank=True, null=True, choices=[
                    ('hours', 'Hours'), ('days', 'Days'), ('weeks', 'Weeks'), ('months', 'Months')])),
                ('frequency_value', models.IntegerField(blank=True, null=True)),
                ('next_restart', models.DateTimeField(blank=True, null=True, db_index=True)),
                ('notifications', models.IntegerField(blank=True, null=True, default=3)),
                ('on_finish', models.CharField(max_length=50, blank=True, default='open', choices=[
                    ('open', 'Open'), ('close', 'Close'), ('repeat', 'Repeat')])),
                ('permissions', models.IntegerField(blank=True, null=True, default=19)),
                ('repeat_until', models.DateTimeField(blank=True, null=True)),
                ('state', models.CharField(max_length=50, default='open', choices=[
                    ('scripted', 'Scripted'), ('assisted', 'Assisted'), ('closed', 'Closed'), ('open', 'Open')])),
                ('type', models.CharField(max_length=50, db_index=True, default='chat', choices=[
                    ('chat', 'Chat'), ('survey', 'Survey'), ('tracker', 'Tracker')])),
                ('updated', models.DateTimeField(db_index=True)),
                ('automated_sender', models.ForeignKey(blank=True, null=True, related_name='automated_threads_sent_by',
                                                       to=settings.AUTH_USER_MODEL, db_index=False,
                                                       on_delete=django.db.models.deletion.CASCADE)),
                ('initial_question', models.ForeignKey(blank=True, null=True, related_name='states_inited_with',
                                                       to='chat_api.Question', db_index=False,
                                                       on_delete=django.db.models.deletion.CASCADE)),
                ('question', models.ForeignKey(blank=True, null=True, related_name='states_with',
                                               to='chat_api.Question', db_index=False,
                                               on_delete=django.db.models.deletion.CASCADE)),
                ('related_message', models.ForeignKey(blank=True, null=True, editable=False,
                                                      related_name='states_related_with', to='chat_api.Message',
                                                      db_index=False, on_delete=django.db.models.deletion.CASCADE)),
                ('schema', models.ForeignKey(blank=True, null=True, to='chat_api.Schema', db_index=False,
                                             on_delete=django.db.models.deletion.CASCADE)),
                ('thread', models.ForeignKey(related_name='users', to='chat_api.Thread',
                                             on_delete=django.db.models.deletion.CASCADE)),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=django.db.models.deletion.CASCADE)),
            ],
        ),
        migrations.AlterUniqueTogether(
            name='schema',
            unique_together=set([('name', 'version')]),
        ),
        migrations.AddField(
            model_name='question',
            name='schema',
            field=models.ForeignKey(to='chat_api.Schema', on_delete=django.db.models.deletion.CASCADE),
        ),
        migrations.AddField(
            model_name='message',
            name='related_question',
            field=models.ForeignKey(blank=True, null=True, to='chat_api.Question',
                                    on_delete=django.db.models.deletion.CASCADE),
        ),
        migrations.AddField(
            model_name='message',
            name='sender',
            field=models.ForeignKey(blank=True, null=True, to=settings.AUTH_USER_MODEL, db_index=False,
                                    on_delete=django.db.models.deletion.CASCADE),
        ),
        migrations.AddField(
            model_name='message',
            name='thread',
            field=models.ForeignKey(to='chat_api.Thread', on_delete=django.db.models.deletion.CASCADE),
        ),
        migrations.AddField(
            model_name='group',
            name='schema',
            field=models.ForeignKey(related_name='groups', to='chat_api.Schema',
                                    on_delete=django.db.models.deletion.CASCADE),
        ),
        migrations.AddField(
            model_name='attachmenttemplate',
            name='question',
            field=models.ForeignKey(blank=True, null=True, to='chat_api.Question',
                                    on_delete=django.db.models.deletion.CASCADE),
        ),
        migrations.AddField(
            model_name='attachment',
            name='message',
            field=models.ForeignKey(to='chat_api.Message', on_delete=django.db.models.deletion.CASCADE),
        ),
        migrations.AddField(
            model_name='answer',
            name='question',
            field=models.ForeignKey(related_name='answers', to='chat_api.Question',
                                    on_delete=django.db.models.deletion.CASCADE),
        ),
        migrations.AlterUniqueTogether(
            name='userthread',
            unique_together=set([('user', 'thread')]),
        ),
        migrations.AlterUniqueTogether(
            name='question',
            unique_together=set([('qid', 'schema')]),
        ),
        migrations.AlterUniqueTogether(
            name='group',
            unique_together=set([('position', 'schema'), ('name', 'schema')]),
        ),
        migrations.AlterUniqueTogether(
            name='answer',
            unique_together=set([('position', 'question')]),
        ),
    ]
