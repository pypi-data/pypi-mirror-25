# -*- coding: utf-8 -*-
from chat_api.chat.models import Attachment, Message, Thread, UnreadMessage, UserThread, VariableModification
from chat_api.chat.optimizations import get_thread_optimization_option, UserThreadsPool
from chat_api.chat.signals import thread_state_changed
from chat_api.common import AttachmentSerializerMixin
from chat_api.schemas.models import Question
from chat_api.schemas.serializers import QuestionSerializer
from chat_api.settings import chat_settings
from chat_api.utils.serializer_fields import JSONField
from collections import OrderedDict
from dateutil.parser import parse
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from drf_tweaks.serializers import ModelSerializer, pass_context, Serializer
from html import escape
from rest_framework import serializers
from rest_framework.compat import is_authenticated, set_many
from rest_framework.utils import model_meta
from threading import current_thread

import traceback

User = get_user_model()


class GetUserThreadMixin(object):
    def get_user_thread(self, return_default=False):
        if not hasattr(self, "user_thread"):
            request = self.context.get("request", {})
            view = self.context.get("view", {})
            self.user_thread = None
            if request and is_authenticated(request.user) and view:
                self.user_thread = UserThreadsPool.get_user_thread(
                    request=request, thread_id=view.kwargs["thread_id"], user=request.user,
                    return_default=return_default
                )
        return self.user_thread


class AttachmentSerializer(AttachmentSerializerMixin, ModelSerializer):
    content_type_name = serializers.SerializerMethodField()
    options = JSONField(required=False)
    thumbnail = serializers.SerializerMethodField()
    src = serializers.SerializerMethodField()
    file_content = serializers.CharField(required=False, max_length=100000000, write_only=True, allow_blank=True)

    def get_content_type_name(self, obj):
        if obj.content_type_id:
            return obj.content_type.name
        return None

    def prepare_validated_data_for_save(self, validated_data):
        validated_data = self.pre_save(validated_data)
        return self.generate_thumbnail(validated_data)

    def update(self, instance, validated_data):
        self.prepare_validated_data_for_save(validated_data)
        return super(AttachmentSerializer, self).update(instance, validated_data)

    def create(self, validated_data):
        self.prepare_validated_data_for_save(validated_data)
        return super(AttachmentSerializer, self).create(validated_data)

    class Meta:
        model = Attachment
        fields = [
            "title", "message", "description", "src", "id", "thumbnail", "options", "object_id", "content_type", "type",
            "content_type_name", "file_content"
        ]
        read_only_fields = [
            "id", "message"
        ]

    required_fields = [
        "message", "type"
    ]


class BaseMessageMixin(object):
    def get_attachments_data(self, obj):
        if obj.has_attachments:
            if not hasattr(obj, "_attachments"):
                obj._attachments = list(obj.attachments.all())
            return AttachmentSerializer(obj._attachments, many=True,
                                        context=pass_context("attachments_data", self.context)).data
        return []


class MessageListSerializer(ModelSerializer, BaseMessageMixin):
    attachments_data = AttachmentSerializer(source="attachments", many=True, read_only=True)
    break_state = serializers.BooleanField(write_only=True, required=False)
    is_own = serializers.SerializerMethodField()
    sender_data = chat_settings.ACCOUNT_SERIALIZER(source="sender", read_only=True, required=False)
    is_read = serializers.SerializerMethodField()
    meta = JSONField(required=False)

    def get_is_read(self, obj):
        if "request" in self.context:
            try:
                # OPTIMIZATION FIXME: move it outside
                UnreadMessage.objects.get(message_id=obj.pk, user=self.context["request"].user).delete()
                return False
            except UnreadMessage.DoesNotExist:
                pass
        return True

    def get_is_own(self, obj):
        request = self.context.get("request", {})
        if request and is_authenticated(request.user) and request.user.id == obj.sender_id:
            return True
        return False

    class Meta:
        model = Message
        fields = [
            "related_question", "updated", "meta", "created", "is_read", "has_attachments", "thread", "sender", "id",
            "text", "type", "break_state", "sender_data", "attachments_data", "is_own"
        ]
        read_only_fields = [
            "related_question", "updated", "sender_data", "created", "has_attachments", "thread", "sender", "id"
        ]

    required_fields = [
        "thread", "type"
    ]


class AnswerValidationMixin(object):
    def validate_text(self, value):
        return escape(value)

    def answer_validation(self, data, question):
        errors = {}

        answers = data.get("answers", None)
        text = data.get("text", "")
        qtype = question.type

        if qtype in (Question.TYPE_CHOICE, Question.TYPE_MULTICHOICE):
            if not question.choice_open and text:
                errors["text"] = ["WRONG_STATE"]
            if not answers:
                errors["answers"] = ["REQUIRED"]
            else:
                if len(answers) > 1:
                    if qtype == Question.TYPE_CHOICE:
                        errors["answers"] = ["TOO_MANY"]
                    elif qtype == Question.TYPE_MULTICHOICE and any(answer.exclusive for answer in answers):
                        errors["answers"] = ["EXCLUSIVE"]

            if answers and any(answer.question_id != question.pk for answer in answers):
                errors["answers"] = ["WRONG_VALUE"]
        else:
            if answers:
                errors["answers"] = ["WRONG_STATE"]
            if not text:
                errors["text"] = ["REQUIRED"]

            if qtype != Question.TYPE_TEXT:
                text = text.strip()
                if qtype in [Question.TYPE_DATE, Question.TYPE_TIME, Question.TYPE_DATETIME]:
                    try:
                        parse(text)
                    except ValueError:
                        errors["text"] = ["WRONG_VALUE"]
                elif qtype == Question.TYPE_INT:
                    try:
                        int(text)
                    except ValueError:
                        errors["text"] = ["WRONG_VALUE"]
                elif qtype == Question.TYPE_FLOAT:
                    try:
                        float(text)
                    except ValueError:
                        errors["text"] = ["WRONG_VALUE"]
                elif qtype == Question.TYPE_RANGE:
                    try:
                        f = float(text)
                        if not question.range_from <= f <= question.range_to:
                            errors["text"] = ["WRONG_VALUE"]
                    except ValueError:
                        errors["text"] = ["WRONG_VALUE"]

        return errors


class MessageCreateSerializer(ModelSerializer, BaseMessageMixin, AnswerValidationMixin, GetUserThreadMixin):
    attachments_data = serializers.SerializerMethodField()
    break_state = serializers.BooleanField(write_only=True, required=False)
    is_own = serializers.SerializerMethodField()
    sender_data = chat_settings.ACCOUNT_SERIALIZER(source="sender", read_only=True, required=False)
    thread_data = serializers.SerializerMethodField()
    is_read = serializers.SerializerMethodField()
    meta = JSONField(required=False)
    attachments = AttachmentSerializer(write_only=True, many=True, required=False)
    question = serializers.PrimaryKeyRelatedField(queryset=Question.objects.all(), required=False, write_only=True)

    def get_is_read(self, obj):  # create
        return True

    def get_thread_data(self, obj):
        user_thread = self.get_user_thread()
        if user_thread:
            return ThreadSerializer(user_thread, context=pass_context("thread_data", self.context)).data
        return {}

    def get_is_own(self, obj):
        return True

    def validate_question(self, value):
        user_thread = self.get_user_thread()
        if user_thread:
            if user_thread.schema_id != value.schema_id:
                raise serializers.ValidationError("QUESTION_FROM_WRONG_SCHEMA")
        return value

    def validate_break_state(self, value):
        if value:  # only if it is True
            user_thread = self.get_user_thread()
            if user_thread and user_thread.permissions & UserThread.PERMISSION_THREAD_BREAK_STATE:
                return value
            raise serializers.ValidationError("NO_PERMISSIONS")
        return value

    def create(self, data):
        next_qid = data.pop("next_qid", None)
        question = data.pop("question", None)

        # state breaking
        break_state = data.pop("break_state", False)
        view = self.context.get("view", {})
        if break_state and view:
            UserThread.objects.filter(
                thread_id=view.kwargs["thread_id"],
                state__in=(UserThread.STATE_SCRIPTED, UserThread.STATE_SCRIPTED_FE_CONTROLLED)
            ).update(state=UserThread.STATE_OPEN)

        # create message
        user_thread = self.get_user_thread()
        if user_thread:
            if user_thread.state == UserThread.STATE_SCRIPTED and user_thread.question_id:
                data["related_question_id"] = user_thread.question_id
            elif user_thread.state == UserThread.STATE_SCRIPTED_FE_CONTROLLED:
                Message.create_from_question(user_thread, question, None)
                data["related_question_id"] = question.pk
            elif user_thread.state == UserThread.STATE_CLOSED:
                # sending new message should open if closed (if has the PERMISSION_THREAD_REOPEN)
                UserThread.objects.filter(thread_id=user_thread.thread_id).update(state=UserThread.STATE_OPEN)

        attachments = []
        if "attachments" in data and data["attachments"]:
            for attachment_data in data.pop("attachments"):
                attachment_serializer = AttachmentSerializer(data=attachment_data)
                if attachment_serializer.is_valid():
                    processed_attachment_data = attachment_serializer.prepare_validated_data_for_save(
                        attachment_serializer.validated_data
                    )
                    attachments.append(Attachment(**processed_attachment_data))

        # this part is copied from rest_framework so it could be modified to handle attachment creation
        info = model_meta.get_field_info(Message)
        many_to_many = {}
        for field_name, relation_info in info.relations.items():
            if relation_info.to_many and (field_name in data):
                many_to_many[field_name] = data.pop(field_name)
        try:
            if attachments:
                instance = Message.create_with_attachments(attachments=attachments, **data)
            else:
                instance = Message.objects.create(**data)
        except TypeError:
            tb = traceback.format_exc()
            msg = (
                'Got a `TypeError` when calling `%s.objects.create()`. '
                'This may be because you have a writable field on the '
                'serializer class that is not a valid argument to '
                '`%s.objects.create()`. You may need to make the field '
                'read-only, or override the %s.create() method to handle '
                'this correctly.\nOriginal exception was:\n %s' %
                (
                    Message.__name__,
                    Message.__name__,
                    self.__class__.__name__,
                    tb
                )
            )
            raise TypeError(msg)

        # Save many-to-many relationships after the instance is created.
        if many_to_many:
            for field_name, value in many_to_many.items():
                if field_name == "answers":
                    do_not_add_answers = bool(user_thread) and get_thread_optimization_option(
                        user_thread.type, "SEND_SIGNAL_INSTEAD_ADDING_ANSWERS"
                    )
                    if do_not_add_answers:  # TODO: filter by rejected
                        from chat_api.chat.signals import chosen_answers_signal

                        chosen_answers_signal.send(message=instance, answers=value, sender=self.__class__)

                        limit_variables_notifications = get_thread_optimization_option(
                            user_thread.type, "LIMIT_VARIABLES_MODIFICATIONS_TO"
                        )
                        filtered_answers = []
                        for answer in value:
                            if answer.variable_modifications:
                                if limit_variables_notifications:
                                    for variable_modification in answer.variable_modifications:
                                        if variable_modification[0] in limit_variables_notifications:
                                            filtered_answers.append(answer)
                                            break
                                else:
                                    filtered_answers.append(answer)

                        if filtered_answers:
                            value = filtered_answers  # normal procedure, just with
                        else:
                            continue

                    set_many(instance, field_name, value)

                    answers_map = {}
                    for answer in value:
                        if answer.variable_modifications:
                            answers_map[answer.pk] = answer
                    if answers_map:
                        for mat in instance.answers.through.objects.filter(message=instance,
                                                                           answer_id__in=answers_map.keys()):
                            VariableModification.objects.create(
                                variable_modifications=answers_map[mat.answer_id].variable_modifications,
                                user_thread=user_thread,
                                related_message_answer_id=mat.pk
                            )
                else:
                    set_many(instance, field_name, value)

        # moving on schema - will generate another message (so also WS)
        if user_thread and next_qid is not None:
            if not get_thread_optimization_option(user_thread.type, "NO_MOVE_TO_NEXT_QID") or next_qid == -1:
                user_thread.move_to_qid(next_qid)

        return instance

    def validate(self, data):
        errors = {}
        user_thread = self.get_user_thread()
        answers = data.get("answers", None)

        if (user_thread and user_thread.state == UserThread.STATE_CLOSED and
                not user_thread.permissions & UserThread.PERMISSION_THREAD_REOPEN):
            raise serializers.ValidationError("THREAD_IS_CLOSED")

        if user_thread and user_thread.state in (UserThread.STATE_SCRIPTED, UserThread.STATE_SCRIPTED_FE_CONTROLLED):
            if user_thread.state == UserThread.STATE_SCRIPTED:
                question = user_thread.question
            elif user_thread.state == UserThread.STATE_SCRIPTED_FE_CONTROLLED:
                question = data.get("question", None)
                if not question:
                    errors["question"] = ["REQUIRED"]

            if question:
                if question.type == Question.TYPE_CONTROL:
                    self.confirmation_only = True
                    self.next_qid = question.next_qid
                else:
                    errors.update(self.answer_validation(data, question))

            if not errors:
                text = data.get("text", None)
                data["next_qid"] = question.next_qid

                if question.type in (Question.TYPE_CHOICE, Question.TYPE_MULTICHOICE):
                    data["text"] = ", ".join(answer.text for answer in answers)
                    if question.choice_open and text:
                        data["text"] += ", " + text

                    data["next_qid"] = answers[0].next_qid
        elif answers:
            errors["answers"] = ["WRONG_STATE"]

        if errors:
            raise serializers.ValidationError(errors)
        return data

    class Meta:
        model = Message
        fields = [
            "related_question", "updated", "meta", "created", "is_read", "has_attachments", "thread", "sender", "id",
            "answers", "text", "type", "break_state", "sender_data", "attachments_data", "is_own", "thread_data",
            "attachments", "question"
        ]
        read_only_fields = [
            "related_question", "updated", "sender_data", "created", "has_attachments", "is_own", "thread",
            "sender", "attachments_data", "id"
        ]

    required_fields = [
        "thread", "type"
    ]


class ThreadMixin(object):
    def validate_repeat_until(self, value):
        if value <= timezone.now():
            raise serializers.ValidationError("REPEAT_UNTIL_MUST_BE_IN_FUTURE")
        return value

    def validate_common(self, data):
        errors = {}
        if "schema" in data and data["schema"]:
            if "state" not in data or data["state"] not in (UserThread.STATE_SCRIPTED,
                                                            UserThread.STATE_SCRIPTED_FE_CONTROLLED,
                                                            UserThread.STATE_ASSISTED):
                errors["state"] = ["WRONG_STATE_FOR_SCHEMA"]

        if "repeat_until" in data and data["repeat_until"]:
            if "frequency_unit" not in data or data["frequency_unit"] is None:
                errors["frequency_unit"] = ["REQUIRED"]

            if "frequency_value" in data and data["frequency_value"] is not None:
                if data["frequency_value"] < 1:
                    errors["frequency_value"] = ["FREQUENCY_VALUE_MUST_BE_POSITIVE"]
            else:
                errors["frequency_value"] = ["REQUIRED"]

        return errors

    def get_last_message_data(self, obj):
        if obj.last_message:
            context = {}
            if "user_id" in self.context:
                context["user_id"] = self.context["user_id"]
            if "request" in self.context:
                # request has to be passed to enable drf_tweaks include_fields
                context["request"] = self.context["request"]
                context["user_id"] = self.context["request"].user.pk
            return MessageSerializer(obj.last_message, context=pass_context("last_message_data", context)).data
        return None

    def get_id(self, obj):
        return obj.thread_id

    def get_users_data(self, obj):
        context_to_pass = pass_context("users_data", self.context)
        if "request" in self.context and UserThreadsPool.is_mapped(self.context["request"], obj.thread_id):
            return chat_settings.ACCOUNT_SERIALIZER(
                UserThreadsPool.get_users(self.context["request"], obj.thread_id), many=True, context=context_to_pass
            ).data
        elif hasattr(current_thread, "request") and UserThreadsPool.is_mapped(current_thread.request, obj.thread_id):
            return chat_settings.ACCOUNT_SERIALIZER(UserThreadsPool.get_users(
                current_thread.request,
                thread_id=obj.thread_id,
            ), many=True, context=context_to_pass).data

        return ThreadAccountSerializer(
            obj.thread.users, many=True, context=context_to_pass).data


class ThreadAccountSerializer(ModelSerializer):
    class Meta:
        model = UserThread
        fields = []

    def to_representation(self, obj):
        # enable using the serializer on User objects
        if type(obj) == UserThread:
            user = obj.user
        else:
            user = obj

        data = super(ThreadAccountSerializer, self).to_representation(obj)
        data.update(chat_settings.ACCOUNT_SERIALIZER(user).data)
        return data


class MessageSerializer(ModelSerializer, BaseMessageMixin):
    attachments_data = serializers.SerializerMethodField()
    is_own = serializers.SerializerMethodField()
    sender_data = chat_settings.ACCOUNT_SERIALIZER(source="sender", read_only=True, required=False)
    is_read = serializers.SerializerMethodField()
    meta = JSONField(required=False)

    def get_is_read(self, obj):
        # request is in the context, meaning: we're just querying messages through API - so we should mark them as
        # read
        if "request" in self.context and "user_id" not in self.context:
            try:
                UnreadMessage.objects.get(message_id=obj.pk, user=self.context["request"].user).delete()
                return False
            except UnreadMessage.DoesNotExist:
                pass
        # we're passing user_id to the context - we just check if the message is unread
        elif self.context and "user_id" in self.context:
            if hasattr(current_thread, "request"):
                is_read = UserThreadsPool.get_is_read(current_thread.request, obj, self.context["user_id"])
                if is_read is not None:
                    return is_read
            try:
                UnreadMessage.objects.get(message_id=obj.pk, user_id=self.context["user_id"])
                return False
            except UnreadMessage.DoesNotExist:
                pass
        return True

    def get_is_own(self, obj):
        request = self.context.get("request", None)
        if request:
            if is_authenticated(request.user) and request.user.id == obj.sender_id:
                return True
        elif hasattr(obj, "user_thread"):
            return obj.user_thread.user_id == obj.sender_id
        elif self.context and "user_id" in self.context:
            return self.context["user_id"] == obj.sender_id
        return False

    class Meta:
        model = Message
        fields = [
            "related_question", "updated", "meta", "created", "is_read", "has_attachments", "thread", "sender", "id",
            "text", "type", "sender_data", "attachments_data", "is_own"
        ]
        read_only_fields = [
            "related_question", "updated", "sender_data", "created", "has_attachments", "is_own", "type", "thread",
            "sender", "attachments_data", "id"
        ]

    required_fields = [
        "thread", "type"
    ]


class ThreadListCreateSerializer(ModelSerializer, ThreadMixin):
    question_data = QuestionSerializer(source="question", read_only=True)
    title = serializers.CharField(required=False)
    users_data = ThreadAccountSerializer(source="thread.users", many=True, read_only=True)
    id = serializers.SerializerMethodField()
    unread = serializers.SerializerMethodField()
    last_message_data = serializers.SerializerMethodField()

    def get_unread(self, obj):
        if "request" in self.context:
            return UnreadMessage.objects.filter(thread_id=obj.thread_id, user=self.context["request"].user).count()
        return 0

    def create(self, data):
        title = data.pop("title", "")
        thread = Thread.objects.create(title=title, type=data["type"])
        data["thread"] = thread
        data["permissions"] = UserThread.PERMISSIONS_CREATOR_DEFAULT
        return super(ThreadListCreateSerializer, self).create(data)

    def validate(self, data):
        errors = self.validate_common(data)

        if errors:
            raise serializers.ValidationError(errors)
        return data

    class Meta:
        model = UserThread
        fields = [
            "id", "type", "created", "updated", "permissions", "notifications", "schema", "state", "question", "unread",
            "on_finish", "title", "users_data", "frequency_unit", "frequency_value", "next_restart", "automated_sender",
            "initial_question", "repeat_until", "question_data", "related_message", "last_message_data"
        ]
        read_only_fields = [
            "updated", "created", "users_data", "type", "permissions"
        ]

    required_fields = [
        "type"
    ]


class ThreadSerializer(ModelSerializer, ThreadMixin):
    question_data = QuestionSerializer(source="question", read_only=True)
    title = serializers.CharField(required=False)
    users_data = serializers.SerializerMethodField()
    id = serializers.SerializerMethodField()
    unread = serializers.SerializerMethodField()
    last_message_data = serializers.SerializerMethodField()
    variables_pool = JSONField(read_only=True)

    def get_unread(self, obj):
        if "request" in self.context:
            return UnreadMessage.objects.filter(thread_id=obj.thread_id, user=self.context["request"].user).count()
        elif "user_id" in self.context:
            if hasattr(current_thread, "request"):
                count = UserThreadsPool.unread_number(current_thread.request, obj.thread_id, self.context["user_id"])
                if count is not None:
                    return count
            return UnreadMessage.objects.filter(thread_id=obj.thread_id, user=self.context["user_id"]).count()
        return 0

    def update(self, instance, data):
        title = data.pop("title", None)
        if title is not None and title != instance.thread.title:
            instance.thread.title = title
            instance.thread.save()

        state = data.get("state")
        if state and state != instance.state:
            UserThread.objects.filter(thread=instance.thread).update(state=state)
            if "request" in self.context:
                thread_state_changed.send(sender=Thread, thread=instance.thread, state=state,
                                          previous_state=instance.state, user=self.context["request"].user)

        return super(ThreadSerializer, self).update(instance, data)

    class Meta:
        model = UserThread
        fields = [
            "id", "type", "created", "updated", "permissions", "notifications", "schema", "state", "question", "unread",
            "on_finish", "initial_question", "repeat_until", "frequency_unit", "frequency_value", "next_restart",
            "automated_sender", "title", "users_data", "question_data", "related_message", "last_message_data",
            "variables_pool"
        ]
        read_only_fields = [
            "updated", "question_data", "created", "users_data", "next_restart", "type", "schema", "question",
            "permissions", "on_finish", "initial_question", "repeat_until", "frequency_unit", "frequency_value",
            "automated_sender", "variables_pool"
        ]

    required_fields = [
        "type"
    ]


class ThreadUserSerializer(ModelSerializer):
    users_data = ThreadAccountSerializer(source="user", read_only=True)
    permissions = serializers.IntegerField(default=UserThread.PERMISSIONS_DEFAULT)

    def create(self, validated_data):
        thread = Thread.objects.get(pk=self.context["thread_id"])
        return UserThread.objects.create(
            thread=thread, created=thread.created, updated=thread.updated, notifications=0,
            last_message=thread.last_message, **validated_data
        )

    def to_representation(self, instance):
        fields = super(ThreadUserSerializer, self).to_representation(instance)
        user_thread = UserThreadsPool.get_user_thread(
            request=self.context["request"], thread_id=self.context["thread_id"], user=self.context["request"].user)
        if not UserThread.PERMISSION_THREAD_CONTROL_OTHERS & user_thread.permissions:
            filtered_fields = OrderedDict()
            for field_name in fields.keys():
                if field_name not in ThreadUserSerializer.Meta.control_others_fields:
                    filtered_fields[field_name] = fields[field_name]

            return filtered_fields

        return fields

    def get_extra_kwargs(self):
        extra_kwargs = super(ThreadUserSerializer, self).get_extra_kwargs()
        if self.instance:
            # disallow editing user field on update (it is allowed on create)
            kwargs = extra_kwargs.get("user", {})
            kwargs["read_only"] = True
            extra_kwargs["user"] = kwargs

        return extra_kwargs

    def validate_user(self, value):
        if UserThread.objects.filter(user=value, thread_id=self.context["thread_id"]).exists():
            raise serializers.ValidationError({"user": _("User already exists in this thread.")})

        return value

    def validate_permissions(self, value):
        user_thread = UserThread.objects.get(thread_id=self.context["thread_id"], user=self.context["request"].user)
        if value != (value & user_thread.permissions):
            raise serializers.ValidationError(
                {"permissions": _("Cannot set higher permissions that the request user possess.")})

        return value

    def validate_state(self, value):
        # allow only one scripted user thread
        scripted_statuses = [UserThread.STATE_SCRIPTED, UserThread.STATE_SCRIPTED_FE_CONTROLLED]
        query = UserThread.objects.filter(
            thread_id=self.context["thread_id"], state__in=scripted_statuses)
        if self.instance:
            query = query.exclude(pk=self.instance.pk)

        if value in scripted_statuses and query.exists():
            raise serializers.ValidationError({
                "state": _("Only one scripted mode per thread is allowed.")})

        return value

    class Meta:
        model = UserThread
        control_others_fields = [
            "automated_sender", "frequency_unit", "frequency_value", "repeat_until", "initial_question",
            "on_finish", "schema", "state"
        ]
        fields = ["user", "permissions", "users_data"] + control_others_fields


class MessageWithThreadSerializer(MessageSerializer, BaseMessageMixin):
    attachments_data = serializers.SerializerMethodField()
    thread_data = serializers.SerializerMethodField()
    is_read = serializers.SerializerMethodField()
    meta = JSONField(required=False)

    def get_is_read(self, obj):
        user_thread = getattr(obj, "user_thread", None)
        if user_thread and user_thread.notifications & UserThread.NOTIFIACTIONS_UNREAD:
            return obj.sender_id == user_thread.user_id
        return True

    def get_thread_data(self, obj):
        user_thread = getattr(obj, "user_thread", None)
        if user_thread:
            return ThreadSerializer(user_thread, context={"user_id": user_thread.user_id}).data
        return {}

    def to_representation(self, obj):
        if obj.deleted:
            return {
                "id": obj.id,
                "thread": obj.thread_id,
                "deleted": True
            }
        return super(MessageWithThreadSerializer, self).to_representation(obj)

    class Meta:
        model = Message
        fields = [
            "related_question", "updated", "meta", "created", "is_read", "has_attachments", "thread", "sender",
            "id", "text", "type", "sender_data", "attachments_data", "is_own", "thread_data"
        ]
        read_only_fields = [
            "related_question", "updated", "sender_data", "created", "has_attachments", "is_own", "type", "thread",
            "sender", "attachments_data", "id"
        ]

    required_fields = [
        "thread", "type"
    ]


class DotsSerializer(Serializer):
    thread = serializers.IntegerField()
    length = serializers.IntegerField()
    sender_data = chat_settings.ACCOUNT_SERIALIZER(read_only=True, required=False)


class RollbackSerializer(GetUserThreadMixin, Serializer):
    message = serializers.PrimaryKeyRelatedField(queryset=Message.objects.all(), required=False)
    question = serializers.PrimaryKeyRelatedField(queryset=Question.objects.all(), required=False)

    def validate_question(self, value):
        user_thread = self.get_user_thread()
        if value.schema_id != user_thread.schema_id:
            raise serializers.ValidationError("QUESTION_FROM_WRONG_SCHEMA")

        if value.type == value.TYPE_CONTROL:
            raise serializers.ValidationError("QUESTION_TYPE_CONTROL")

        question_message = Message.objects.filter(thread_id=user_thread.thread_id,
                                                  related_question=value).order_by("created").first()
        if not question_message:
            raise serializers.ValidationError("NO_SUCH_MESSAGE")
        self.question_message = question_message  # to not call it twice
        return value

    def validate_message(self, value):
        user_thread = self.get_user_thread()
        if value.thread_id != user_thread.thread_id or not value.related_question \
                or value.related_question.show_as_type != value.type:
            raise serializers.ValidationError("NOT_A_QUESTION")
        return value

    def validate(self, data):
        errors = {}
        user_thread = self.get_user_thread()
        if user_thread.state not in (UserThread.STATE_SCRIPTED, UserThread.STATE_SCRIPTED_FE_CONTROLLED):
            errors["non_fields_errors"] = ["WRONG_STATE"]
        else:
            if user_thread.state == UserThread.STATE_SCRIPTED:
                if "message" not in data:  # default - rollback by one step
                    if user_thread.state == UserThread.STATE_SCRIPTED_FE_CONTROLLED:
                        errors["message"] = ["REQUIRED"]
                    else:
                        if not user_thread.related_message_id:
                            errors["non_fields_errors"] = ["WRONG_STATE"]
                        elif not user_thread.related_message.predecessor_id:
                            errors["non_fields_errors"] = ["AT_THE_BEGINNING"]
            elif user_thread.state == UserThread.STATE_SCRIPTED_FE_CONTROLLED:
                if "question" not in data:
                    errors["question"] = ["REQUIRED"]

        if errors:
            raise serializers.ValidationError(errors)

        return data
