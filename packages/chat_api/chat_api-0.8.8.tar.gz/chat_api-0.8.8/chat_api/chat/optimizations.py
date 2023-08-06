# -*- coding: utf-8 -*-
from chat_api.settings import chat_settings
from rest_framework.request import Request


def get_thread_optimization_option(thread_type, option):
    if thread_type in chat_settings.OPTIMIZATIONS_BY_THREAD_TYPE:
        return chat_settings.OPTIMIZATIONS_BY_THREAD_TYPE[thread_type].get(option, None)
    return None


class UserThreadsPool(object):
    """Pool to keep UserThread and pass them through threading.

    UserThreads, users they keep, and methods related with them are uesed on many levels of chat_api.
    It is best to keep them from the beginning (permissions) through the serializers ending with websockets.
    """

    @classmethod
    def _extract_django_request(cls, request):
        """Make sure we're operating on django requests, not rest framework requests."""
        if isinstance(request, Request):
            return request._request
        return request

    @classmethod
    def _get_user_threads_pool(cls, request, thread_id):
        if not hasattr(request, "_chat_api_user_threads_pool"):
            request._chat_api_user_threads_pool = {}

        if int(thread_id) not in request._chat_api_user_threads_pool:
            from chat_api.chat.models import UserThread

            user_threads = list(UserThread.objects.select_related(
                "user", "last_message", "thread", "thread__last_message"
            ).filter(thread_id=thread_id))
            request._chat_api_user_threads_pool[int(thread_id)] = dict((x.user_id, x) for x in user_threads)
            if user_threads:
                if not hasattr(request, "_chat_api_thread"):
                    request._chat_api_thread = {}
                request._chat_api_thread[int(thread_id)] = user_threads[0].thread
        return request._chat_api_user_threads_pool[int(thread_id)]

    @classmethod
    def get_thread(cls, request, thread_id):
        if not hasattr(request, "_chat_api_thread"):
            request._chat_api_thread = {}

        if thread_id not in request._chat_api_thread:
            from chat_api.chat.models import Thread

            request._chat_api_thread[int(thread_id)] = Thread.objects.select_related("last_message").get(pk=thread_id)
        return request._chat_api_thread[int(thread_id)]

    @classmethod
    def get_thread_if_exists(cls, request, thread_id):
        if hasattr(request, "_chat_api_thread"):
            return request._chat_api_thread.get(int(thread_id), None)
        return None

    @classmethod
    def get_user_thread(cls, request, thread_id, user, return_default=False):
        """Gets user thread while creating pool if necessary."""
        request = cls._extract_django_request(request)
        user_threads_pool = cls._get_user_threads_pool(request, thread_id)
        if user.pk in user_threads_pool:
            return user_threads_pool[user.pk]
        elif return_default:
            from chat_api.chat.models import UserThread

            thread = cls.get_thread(request, thread_id)
            return UserThread(
                user=user, thread=thread, created=thread.created, updated=thread.updated, notifications=0,
                permissions=UserThread.PERMISSION_MESSAGES_READ | UserThread.PERMISSION_THREAD_READ,
                state=UserThread.STATE_CLOSED, last_message=thread.last_message
            )
        return None

    @classmethod
    def get_user_threads_pool(cls, request, thread_id):
        request = cls._extract_django_request(request)
        return getattr(request, "_chat_api_user_threads_pool", {}).get(int(thread_id), None)

    @classmethod
    def is_mapped(cls, request, thread_id):
        request = cls._extract_django_request(request)
        return hasattr(request, "_chat_api_user_threads_pool") and int(thread_id) in request._chat_api_user_threads_pool

    @classmethod
    def get_users(cls, request, thread_id):
        request = cls._extract_django_request(request)
        if hasattr(request, "_chat_api_user_threads_pool") and int(thread_id) in request._chat_api_user_threads_pool:
            # sorted, so there is some predictability in tests
            return sorted(
                [x.user for x in request._chat_api_user_threads_pool[int(thread_id)].values()], key=lambda x: x.pk
            )
        return []

    @classmethod
    def initialize_unread_states(cls, request, thread_id, unread_obj_created, user_tracking_unread_ids):
        if not hasattr(request, "_unread_states"):
            request._unread_states = {}

        def add_unread_message(um):
            if um.user_id not in request._unread_states[thread_id]:
                request._unread_states[thread_id][um.user_id] = {
                    "total": 1,
                    "messages_ids": {um.message_id}
                }
            else:
                request._unread_states[thread_id][um.user_id]["total"] += 1
                request._unread_states[thread_id][um.user_id]["messages_ids"].add(um.message_id)

        if thread_id not in request._unread_states:
            from chat_api.models import UnreadMessage

            request._unread_states[thread_id] = {}
            if user_tracking_unread_ids:
                for um in UnreadMessage.objects.filter(thread_id=thread_id, user_id__in=user_tracking_unread_ids):
                    add_unread_message(um)

        for um in unread_obj_created:
            add_unread_message(um)

    @classmethod
    def unread_number(cls, request, thread_id, user_id):
        if hasattr(request, "_unread_states") and thread_id in request._unread_states:
            return request._unread_states[thread_id].get(user_id, {}).get("total", 0)
        return None

    @classmethod
    def get_is_read(cls, request, message, user_id):
        if hasattr(request, "_unread_states") and message.thread_id in request._unread_states:
            return message.id in request._unread_states[message.thread_id].get(user_id, {}).get("messages_ids", set())
        return None
