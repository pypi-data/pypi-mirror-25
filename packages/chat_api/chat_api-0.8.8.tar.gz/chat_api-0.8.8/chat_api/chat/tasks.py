from __future__ import absolute_import, unicode_literals
from celery import shared_task


@shared_task
def finish_processing_message_task(message_id):
    from chat_api.chat.models import Thread, Message
    from chat_api.chat.optimizations import get_thread_optimization_option

    message = Message.objects.get(pk=message_id)
    thread = Thread.objects.get(pk=message.thread_id)

    skip_thread_update = get_thread_optimization_option(thread.type, "NO_UPDATES_FOR_LAST_MESSAGE_AND_UPDATED")

    if not skip_thread_update:
        # add checking if message on thread is not newer that the one you want to attach
        Thread.objects.filter(pk=message.thread_id).update(updated=message.updated, last_message=message)

    # index for search
    if not get_thread_optimization_option(thread.type, "NOT_INDEXED"):
        from chat_api.search import index
        index(message)
