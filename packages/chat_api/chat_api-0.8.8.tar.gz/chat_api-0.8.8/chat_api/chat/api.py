# -*- coding: utf-8 -*-
from chat_api.chat.models import Attachment, Message, Thread, ThreadWSSubscription, UserThread
from chat_api.chat.optimizations import get_thread_optimization_option, UserThreadsPool
from chat_api.chat.serializers import (AttachmentSerializer, MessageCreateSerializer, MessageListSerializer,
                                       MessageSerializer, RollbackSerializer, ThreadListCreateSerializer,
                                       ThreadSerializer, ThreadUserSerializer)
from chat_api.search import find_messages
from chat_api.settings import chat_settings
from chat_api.utils.decorators import ClassProperty
from django.contrib.auth import get_user_model
from django.db.models import Q
from django_filters import CharFilter
from django_filters.rest_framework import FilterSet
from drf_tweaks.autodoc import autodoc
from drf_tweaks.autofilter import autofilter
from drf_tweaks.optimizator import AutoOptimizeMixin
from rest_framework import status
from rest_framework.generics import CreateAPIView, ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.response import Response
from rest_framework.serializers import ValidationError

User = get_user_model()


class AccountThreadsListAPI(AutoOptimizeMixin, ListCreateAPIView):
    queryset = UserThread.objects.select_related("question", "thread", "thread__last_message").all()
    serializer_class = ThreadListCreateSerializer
    pagination_class = chat_settings.PAGINATION_THREAD_LIST

    @ClassProperty
    def permission_classes(self):
        return (chat_settings.PERMISSIONS_THREADS_LIST_BY_USER_ID_AND_TYPE,)

    def get_queryset(self):
        queryset = super(AccountThreadsListAPI, self).get_queryset()
        queryset = queryset.filter(
            Q(user_id=self.kwargs["user_id"]) & Q(type=self.kwargs["type"])
        )
        return queryset

    def perform_create(self, serializer):
        serializer.save(user_id=int(self.kwargs["user_id"]), type=self.kwargs["type"])


@autodoc()
class ThreadDetailsAPI(AutoOptimizeMixin, RetrieveUpdateDestroyAPIView):
    queryset = UserThread.objects.all().select_related("question", "thread", "thread__last_message")
    serializer_class = ThreadSerializer
    pagination_class = None

    @ClassProperty
    def permission_classes(self):
        return (chat_settings.PERMISSIONS_THREAD_OBJECT_BY_THREAD_ID,)

    def get_object(self):
        try:
            return self.get_queryset().get(user=self.request.user)
        except UserThread.DoesNotExist:
            # for ppl who are not thread members, yet they still have permissions to get them we will return
            # readonly userthread with "closed" state
            thread = Thread.objects.get(pk=self.kwargs["thread_id"])
            return UserThread(
                user=self.request.user, thread=thread, created=thread.created, updated=thread.updated,
                notifications=0, permissions=UserThread.PERMISSION_MESSAGES_READ | UserThread.PERMISSION_THREAD_READ,
                state=UserThread.STATE_CLOSED, last_message=thread.last_message
            )

    def get_queryset(self):
        queryset = super(ThreadDetailsAPI, self).get_queryset()
        queryset = queryset.filter(
            Q(thread_id=self.kwargs["thread_id"])
        )
        return queryset


class ThreadUsersMixin(object):
    queryset = UserThread.objects.all()
    serializer_class = ThreadUserSerializer

    def get_serializer_context(self):
        context = super(ThreadUsersMixin, self).get_serializer_context()
        context["thread_id"] = self.kwargs["thread_id"]
        return context

    def get_queryset(self):
        return super(ThreadUsersMixin, self).get_queryset().filter(
            Q(thread_id=self.kwargs["thread_id"])
        )


@autodoc()
class ThreadUsersAPI(AutoOptimizeMixin, ThreadUsersMixin, ListCreateAPIView):
    pagination_class = None

    @ClassProperty
    def permission_classes(self):
        return (chat_settings.PERMISSIONS_THREAD_USERS_LIST_BY_THREAD_ID,)


@autodoc()
class ThreadUsersDetailsAPI(AutoOptimizeMixin, ThreadUsersMixin, RetrieveUpdateDestroyAPIView):
    lookup_field = "user_id"

    @ClassProperty
    def permission_classes(self):
        return (chat_settings.PERMISSIONS_THREAD_USERS_OBJECT_BY_THREAD_ID,)


class SearchFilter(FilterSet):
    q = CharFilter(method="filter_q", required=False, label="Search text")

    def filter_q(self, queryset, name, value):
        if value:
            queryset = find_messages(queryset, value)
        return queryset

    class Meta:
        model = Message
        fields = ["q"]


@autodoc()
@autofilter()
class ThreadMessagesListAPI(AutoOptimizeMixin, ListCreateAPIView):
    queryset = Message.objects.all()
    serializer_class = MessageListSerializer
    pagination_class = chat_settings.PAGINATION_THREAD_LIST
    filter_class = SearchFilter

    @ClassProperty
    def permission_classes(self):
        return (chat_settings.PERMISSIONS_MESSAGES_LIST_BY_THREAD_ID,)

    def get_serializer_class(self):
        if hasattr(self, "request") and self.request.method == "POST":
            return MessageCreateSerializer
        return self.serializer_class

    def get_queryset(self):
        queryset = super(ThreadMessagesListAPI, self).get_queryset()
        queryset = queryset.filter(
            Q(thread_id=self.kwargs["thread_id"])
        )
        if chat_settings.CHAT_MESSAGE_FILTER_QUERYSET and self.request:
            queryset = chat_settings.CHAT_MESSAGE_FILTER_QUERYSET(queryset, self.request.user)
        return queryset

    def perform_create(self, serializer):
        thread = UserThreadsPool.get_thread_if_exists(request=self.request, thread_id=self.kwargs["thread_id"])
        if thread:
            serializer.save(thread=thread, sender=self.request.user)
        else:
            serializer.save(thread_id=int(self.kwargs["thread_id"]), sender=self.request.user)

    def get_serializer_context(self):
        context = super(ThreadMessagesListAPI, self).get_serializer_context()
        thread = UserThreadsPool.get_thread_if_exists(request=self.request, thread_id=self.kwargs["thread_id"])
        if thread:
            limit_fields_to = get_thread_optimization_option(thread.type, "LIMIT_FIELDS_TO")
            if limit_fields_to:
                if context.get("fields"):
                    context["fields"] = list(set(context.get("fields", [])) & set(limit_fields_to))
                else:
                    context["fields"] = limit_fields_to
        return context

    def post(self, request, thread_id, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # if only confirmation (control question), we're just moving to the next question, without creating anything
        confirmation_only = getattr(serializer, "confirmation_only", False)
        if confirmation_only:  # TODO: if FE controlled, still add question
            user_thread = serializer.get_user_thread()
            if not get_thread_optimization_option(user_thread.type, "NO_MOVE_TO_NEXT_QID") or serializer.next_qid == -1:
                user_thread.move_to_qid(serializer.next_qid)
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


@autodoc()
@autofilter()
class ThreadMessageAttachmentsListAPI(AutoOptimizeMixin, ListCreateAPIView):
    queryset = Attachment.objects.all()
    serializer_class = AttachmentSerializer
    pagination_class = None

    @ClassProperty
    def permission_classes(self):
        return (chat_settings.PERMISSIONS_ATTACHMENTS_LIST_BY_MESSAGE_ID,)

    def get_queryset(self):
        queryset = super(ThreadMessageAttachmentsListAPI, self).get_queryset()
        queryset = queryset.filter(
            Q(message_id=self.kwargs["message_id"])
        )
        return queryset

    def perform_create(self, serializer):
        serializer.save(message_id=int(self.kwargs["message_id"]))


@autodoc()
class ThreadMessageAttachmentDetailsAPI(AutoOptimizeMixin, RetrieveUpdateDestroyAPIView):
    queryset = Attachment.objects.all()
    serializer_class = AttachmentSerializer
    pagination_class = None

    @ClassProperty
    def permission_classes(self):
        return (chat_settings.PERMISSIONS_ATTACHMENT_OBJECT_BY_MESSAGE_ID,)

    def get_queryset(self):
        queryset = super(ThreadMessageAttachmentDetailsAPI, self).get_queryset()
        queryset = queryset.filter(
            Q(message_id=self.kwargs["message_id"])
        )
        return queryset


@autodoc()
class ThreadMessageDetailsAPI(AutoOptimizeMixin, RetrieveUpdateDestroyAPIView):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    pagination_class = None

    @ClassProperty
    def permission_classes(self):
        return (chat_settings.PERMISSIONS_MESSAGE_OBJECT_BY_THREAD_ID,)

    def get_serializer_context(self):
        context = super(ThreadMessageDetailsAPI, self).get_serializer_context()
        user_thread = UserThreadsPool.get_thread_if_exists(request=self.request, thread_id=self.kwargs["thread_id"])
        if user_thread:
            limit_fields_to = get_thread_optimization_option(user_thread.type, "LIMIT_FIELDS_TO")
            if limit_fields_to:
                if context.get("fields"):
                    context["fields"] = list(set(context.get("fields", [])) & set(limit_fields_to))
                else:
                    context["fields"] = limit_fields_to
        return context

    def get_queryset(self):
        queryset = super(ThreadMessageDetailsAPI, self).get_queryset()
        queryset = queryset.filter(
            Q(thread_id=self.kwargs["thread_id"])
        )
        if chat_settings.CHAT_MESSAGE_FILTER_QUERYSET and self.request:
            queryset = chat_settings.CHAT_MESSAGE_FILTER_QUERYSET(queryset, self.request.user)
        return queryset


@autodoc()
class ThreadWSSubscribeAPI(AutoOptimizeMixin, CreateAPIView):
    pagination_class = None

    @ClassProperty
    def permission_classes(self):
        return (chat_settings.PERMISSIONS_THREAD_WS_SUBSCRIBE,)

    def post(self, request, thread_id, **kwargs):
        ws_subscription, created = ThreadWSSubscription.objects.get_or_create(user=request.user, defaults={
            "thread_id": thread_id
        })
        if not created:
            ws_subscription.thread_id = thread_id
            ws_subscription.save()

        return Response(status=status.HTTP_204_NO_CONTENT)


@autodoc()
class ThreadRollbackAPI(CreateAPIView):
    pagination_class = None
    serializer_class = RollbackSerializer

    @ClassProperty
    def permission_classes(self):
        return (chat_settings.PERMISSIONS_THREAD_ROLLBACK,)

    def post(self, request, thread_id, **kwargs):
        user_thread = UserThreadsPool.get_user_thread(request=request, thread_id=thread_id, user=request.user)
        serializer = self.get_serializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
        except ValidationError as e:
            if e.detail.get("question") and e.detail["question"] == ["QUESTION_TYPE_CONTROL"] \
                    and user_thread.state == UserThread.STATE_SCRIPTED_FE_CONTROLLED:
                return Response(status=status.HTTP_204_NO_CONTENT)
            else:
                raise

        if user_thread.state == UserThread.STATE_SCRIPTED:
            if "message" in serializer.validated_data:
                message_to_rollback_to = serializer.validated_data["message"]
            else:
                message_to_rollback_to = Message.objects.filter(
                    thread_id=user_thread.thread_id,
                    type="automated_message",
                    related_question_id=user_thread.related_message.predecessor_id
                ).order_by("-id").first()

            if message_to_rollback_to:
                Message.objects.filter(thread_id=user_thread.thread_id, id__gt=message_to_rollback_to.pk).delete()
                UserThread.objects.filter(pk=user_thread.pk).update(
                    question=message_to_rollback_to.related_question,
                    related_message=message_to_rollback_to,
                    last_message=message_to_rollback_to
                )  # update, so it does not trigger auto-message send

                # set it to object - to serializer back
                user_thread.question = message_to_rollback_to.related_question
                user_thread.related_message = message_to_rollback_to
                user_thread.last_message = message_to_rollback_to
        elif user_thread.state == UserThread.STATE_SCRIPTED_FE_CONTROLLED:
            Message.objects.filter(thread_id=user_thread.thread_id, id__gte=serializer.question_message.pk).delete()
            last_message = Message.objects.filter(thread_id=user_thread.thread_id).order_by("created").first()
            user_thread.question = serializer.validated_data["question"]
            user_thread.related_message = None
            user_thread.last_message = last_message

        if user_thread.variables_pool:
            user_thread.recalculate_variables_pool()

        return Response(ThreadSerializer(user_thread).data, status=status.HTTP_200_OK)
