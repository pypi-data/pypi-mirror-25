# -*- coding: utf-8 -*-
from chat_api.chat.models import UserThread
from chat_api.chat.optimizations import UserThreadsPool
from chat_api.settings import chat_settings
from rest_framework.permissions import BasePermission, IsAuthenticated


class NoOne(BasePermission):
    """Prevents everyone from accessing given API"""

    def has_permission(self, request, view):
        return False

    def has_object_permission(self, request, view, obj):
        return False


class AttachmentObjectByMessageID(IsAuthenticated):
    def has_permission(self, request, view):
        if not super(AttachmentObjectByMessageID, self).has_permission(request, view):
            return False

        user_thread = UserThreadsPool.get_user_thread(
            request=request, thread_id=view.kwargs["thread_id"], user=request.user
        )
        if user_thread:
            from chat_api.chat.models import Message
            try:
                if request.method == "GET":
                    return user_thread.permissions & user_thread.PERMISSION_THREAD_READ
                else:
                    message = Message.objects.get(pk=view.kwargs["message_id"])
                    if message.sender_id == request.user.pk and request.method in ("PUT", "PATCH", "DELETE"):
                        return user_thread.permissions & user_thread.PERMISSION_MESSAGES_EDIT
            except Message.DoesNotExist:
                pass

        return False

    def has_object_permission(self, request, view, obj):
        return True  # it is checked on "has_permission" already


class SurveyAttachmentObjectByItemID(IsAuthenticated):
    def has_permission(self, request, view):
        if not super(SurveyAttachmentObjectByItemID, self).has_permission(request, view):
            return False

        from chat_api.surveys.models import SurveyItem
        try:
            SurveyItem.objects.get(survey__user=request.user, pk=view.kwargs["item_id"])
            return True
        except SurveyItem.DoesNotExist:
            pass

        return False


class ThreadsListByUserIDAndType(IsAuthenticated):
    def has_permission(self, request, view):
        if not super(ThreadsListByUserIDAndType, self).has_permission(request, view):
            return False

        if ("type" in view.kwargs and view.kwargs["type"] in chat_settings.TYPES_CHAT_LIST_THROUGH_API and
                "user_id" in view.kwargs and view.kwargs["user_id"] == str(request.user.pk)):
            return True

        return False


class ThreadObjectByThreadID(IsAuthenticated):
    def has_permission(self, request, view):
        if not super(ThreadObjectByThreadID, self).has_permission(request, view):
            return False

        user_thread = UserThreadsPool.get_user_thread(
            request=request, thread_id=view.kwargs["thread_id"], user=request.user
        )
        if user_thread:
            if request.method == "GET":
                return user_thread.permissions & user_thread.PERMISSION_THREAD_READ
            elif request.method in ("PUT", "PATCH"):
                return user_thread.permissions & user_thread.PERMISSION_THREAD_EDIT
            elif request.method == "DELETE":
                return user_thread.permissions & user_thread.PERMISSION_THREAD_DELETE

        return False

    def has_object_permission(self, request, view, obj):
        return True  # it is checked on "has_permission" already


class ThreadUsersListByThreadID(IsAuthenticated):
    def has_permission(self, request, view):
        if not super(ThreadUsersListByThreadID, self).has_permission(request, view):
            return False

        user_thread = UserThreadsPool.get_user_thread(
            request=request, thread_id=view.kwargs["thread_id"], user=request.user
        )
        if not user_thread:
            return False

        if request.method == "GET":
            return bool(UserThread.PERMISSION_THREAD_READ & user_thread.permissions)

        if request.method == "POST":
            return bool(UserThread.PERMISSION_THREAD_ADD_USER & user_thread.permissions)

        return False


class ThreadUsersObjectByThreadID(IsAuthenticated):
    def has_permission(self, request, view):
        if not super(ThreadUsersObjectByThreadID, self).has_permission(request, view):
            return False

        user_thread = UserThreadsPool.get_user_thread(
            request=request, thread_id=view.kwargs["thread_id"], user=request.user
        )
        if not user_thread:
            return False

        # do not check if user is accessing their own UserThread
        edited_thread = UserThread.objects.get(thread_id=view.kwargs["thread_id"], user_id=view.kwargs["user_id"])
        if request.user == edited_thread.user:
            return True

        if request.method == "GET":
            return bool(UserThread.PERMISSION_THREAD_READ & user_thread.permissions)

        if request.method == "DELETE":
            return bool(UserThread.PERMISSION_THREAD_REMOVE_USER & user_thread.permissions)

        if request.method == "PATCH":
            return bool(UserThread.PERMISSION_THREAD_CONTROL_OTHERS & user_thread.permissions)

        return False


class AttachmentsListByMessageID(IsAuthenticated):
    def has_permission(self, request, view):
        if not super(AttachmentsListByMessageID, self).has_permission(request, view):
            return False

        user_thread = UserThreadsPool.get_user_thread(
            request=request, thread_id=view.kwargs["thread_id"], user=request.user
        )
        if user_thread:
            from chat_api.chat.models import Message
            try:
                if request.method == "GET":
                    return user_thread.permissions & user_thread.PERMISSION_THREAD_READ
                else:
                    message = Message.objects.get(pk=view.kwargs["message_id"])
                    if message.sender_id == request.user.pk and request.method == "POST":
                        return user_thread.permissions & user_thread.PERMISSION_MESSAGES_CREATE
            except Message.DoesNotExist:
                pass

        return False

    def has_object_permission(self, request, view, obj):
        return True  # it is checked on "has_permission" already


class SurveyItemObjectBySurveyID(IsAuthenticated):
    def has_permission(self, request, view):
        if not super(SurveyItemObjectBySurveyID, self).has_permission(request, view):
            return False

        from chat_api.surveys.models import Survey
        try:
            Survey.objects.get(user=request.user, pk=view.kwargs["survey_id"])
            return True
        except Survey.DoesNotExist:
            pass

        return False


class SurveyAttachmentListByItemID(IsAuthenticated):
    def has_permission(self, request, view):
        if not super(SurveyAttachmentListByItemID, self).has_permission(request, view):
            return False

        from chat_api.surveys.models import SurveyItem
        try:
            SurveyItem.objects.get(survey__user=request.user, pk=view.kwargs["item_id"])
            return True
        except SurveyItem.DoesNotExist:
            pass

        return False


class SurveyObject(IsAuthenticated):
    def has_object_permission(self, request, view, obj):
        return obj.user_id == request.user.pk


class SurveysListByUserID(IsAuthenticated):
    def has_permission(self, request, view):
        if not super(SurveysListByUserID, self).has_permission(request, view):
            return False

        if "user_id" in view.kwargs and view.kwargs["user_id"] == str(request.user.pk):
            return True

        return False


class SurveyItemsListBySurveyID(IsAuthenticated):
    def has_permission(self, request, view):
        if not super(SurveyItemsListBySurveyID, self).has_permission(request, view):
            return False

        from chat_api.surveys.models import Survey
        try:
            Survey.objects.get(user=request.user, pk=view.kwargs["survey_id"])
            return True
        except Survey.DoesNotExist:
            pass

        return False


class SurveysGlobalList(IsAuthenticated):
    pass  # just "IsAuthenticated"


class MessagesListByThreadID(IsAuthenticated):
    def has_permission(self, request, view):
        if not super(MessagesListByThreadID, self).has_permission(request, view):
            return False

        user_thread = UserThreadsPool.get_user_thread(
            request=request, thread_id=view.kwargs["thread_id"], user=request.user
        )
        if user_thread:
            if request.method == "GET":
                return user_thread.permissions & user_thread.PERMISSION_MESSAGES_READ
            elif request.method == "POST":
                return user_thread.permissions & user_thread.PERMISSION_MESSAGES_CREATE

        return False


class MessageObjectByThreadID(IsAuthenticated):
    def has_permission(self, request, view):
        if not super(MessageObjectByThreadID, self).has_permission(request, view):
            return False

        user_thread = UserThreadsPool.get_user_thread(
            request=request, thread_id=view.kwargs["thread_id"], user=request.user
        )
        if user_thread:
            if request.method == "GET":
                return user_thread.permissions & user_thread.PERMISSION_MESSAGES_READ
            elif request.method in ("PUT", "PATCH"):
                return user_thread.permissions & user_thread.PERMISSION_MESSAGES_EDIT
            elif request.method == "DELETE":
                return user_thread.permissions & user_thread.PERMISSION_MESSAGES_DELETE

        return False

    def has_object_permission(self, request, view, obj):
        return True  # it is checked on "has_permission" already


class SchemaObject(IsAuthenticated):
    def has_object_permission(self, request, view, obj):
        return obj.type in chat_settings.TYPES_SCHEMA_GET_THROUGH_API


class SchemaListByType(IsAuthenticated):
    """Checks if user is logged in & if given type can be listed."""

    def has_permission(self, request, view):
        if not super(SchemaListByType, self).has_permission(request, view):
            return False

        if "type" in view.kwargs and view.kwargs["type"] in chat_settings.TYPES_SCHEMA_LIST_THROUGH_API:
            return True

        return False


class ThreadWSSubscribe(IsAuthenticated):
    def has_permission(self, request, view):
        if not super(ThreadWSSubscribe, self).has_permission(request, view):
            return False

        return request.user.is_superuser


class ThreadRollback(IsAuthenticated):
    def has_permission(self, request, view):
        if not super(ThreadRollback, self).has_permission(request, view):
            return False

        user_thread = UserThreadsPool.get_user_thread(
            request=request, thread_id=view.kwargs["thread_id"], user=request.user
        )
        if user_thread:
            return user_thread.permissions & user_thread.PERMISSION_THREAD_ROLLBACK

        return False
