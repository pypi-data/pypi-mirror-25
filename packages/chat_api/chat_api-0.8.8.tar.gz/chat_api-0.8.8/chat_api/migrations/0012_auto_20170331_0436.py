# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import migrations


def update_last_messages(apps, dummy_schema_editor):
    Thread = apps.get_model("chat_api", "Thread")
    UserThread = apps.get_model("chat_api", "UserThread")
    for thread in Thread.objects.all():
        UserThread.objects.filter(thread_id=thread.pk).update(last_message_id=thread.last_message_id)


class Migration(migrations.Migration):

    dependencies = [
        ("chat_api", "0011_userthread_last_message"),
    ]

    operations = [
        migrations.RunPython(update_last_messages),
    ]
