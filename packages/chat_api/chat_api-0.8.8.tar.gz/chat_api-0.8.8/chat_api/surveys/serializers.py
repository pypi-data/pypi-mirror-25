# -*- coding: utf-8 -*-
from chat_api.chat.serializers import AnswerValidationMixin
from chat_api.common import AttachmentSerializerMixin
from chat_api.schemas.serializers import AnswerSerializer, QuestionSerializer
from chat_api.settings import chat_settings
from chat_api.surveys.models import Survey, SurveyAttachment, SurveyItem
from chat_api.utils.serializer_fields import JSONField
from drf_tweaks.serializers import ModelSerializer, pass_context
from rest_framework import serializers


class SurveyAttachmentSerializer(AttachmentSerializerMixin, ModelSerializer):
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
        return super(SurveyAttachmentSerializer, self).update(instance, validated_data)

    def create(self, validated_data):
        self.prepare_validated_data_for_save(validated_data)
        return super(SurveyAttachmentSerializer, self).create(validated_data)

    class Meta:
        model = SurveyAttachment
        fields = [
            "title", "type", "description", "src", "id", "thumbnail", "options", "object_id", "content_type",
            "content_type_name", "file_content", "item"
        ]
        read_only_fields = ["id", "item"]


class BaseSurveyItemMixin(object):
    def get_attachments_data(self, obj):
        if obj.has_attachments:
            return SurveyAttachmentSerializer(obj.attachments.all(), many=True,
                                              context=pass_context("attachments_data", self.context)).data
        return []


class SurveySimpleSerializer(ModelSerializer):
    state = JSONField(read_only=True)

    class Meta:
        model = Survey
        fields = ["schema", "user", "updated", "automated_sender", "id", "created", "state"]
        read_only_fields = ["schema", "user", "updated", "automated_sender", "id", "created", "state"]


class SurveyItemListCreateSerializer(ModelSerializer, BaseSurveyItemMixin, AnswerValidationMixin):
    attachments_data = serializers.SerializerMethodField()
    verify = serializers.BooleanField(write_only=True, required=False)
    meta = JSONField(required=False)
    answers_data = AnswerSerializer(source="answers", many=True, read_only=True)
    survey_data = SurveySimpleSerializer(source="survey", read_only=True)
    related_question_data = QuestionSerializer(source="related_question", read_only=True)

    def validate(self, data):
        errors = {}

        if "related_question" in data:
            related_question = data["related_question"]
            survey_id = self.context["view"].kwargs["survey_id"]
            if SurveyItem.objects.filter(survey_id=survey_id, related_question=related_question).exists():
                errors["related_question"] = ["ALREADY_ANSWERED"]
            else:
                errors = self.answer_validation(data, related_question)

        if errors:
            raise serializers.ValidationError(errors)
        return data

    def create(self, validated_data):
        validated_data.pop("verify", None)
        return super(SurveyItemListCreateSerializer, self).create(validated_data)

    class Meta:
        model = SurveyItem
        fields = [
            "related_question", "updated", "answers", "meta", "created", "has_attachments", "type", "survey", "id",
            "sender", "text", "position", "verify", "attachments_data", "answers_data", "survey_data",
            "related_question_data"
        ]
        read_only_fields = [
            "updated", "meta", "created", "has_attachments", "type", "sender", "attachments_data", "survey_data",
            "id", "position", "survey"
        ]

    required_fields = [
        "related_question"
    ]


class SurveySerializer(ModelSerializer):
    automated_sender_data = chat_settings.ACCOUNT_SERIALIZER(source="automated_sender", read_only=True)
    user_data = chat_settings.ACCOUNT_SERIALIZER(source="user", read_only=True)
    state = JSONField(read_only=True)

    class Meta:
        model = Survey
        fields = [
            "schema", "user", "updated", "automated_sender", "id", "created", "automated_sender_data", "user_data",
            "state"
        ]
        read_only_fields = [
            "schema", "user", "updated", "automated_sender", "created", "user_data", "id", "automated_sender_data",
            "state"
        ]

    required_fields = [
        "user"
    ]


class SurveyItemSerializer(ModelSerializer, BaseSurveyItemMixin):
    attachments_data = serializers.SerializerMethodField()
    sender_data = chat_settings.ACCOUNT_SERIALIZER(read_only=True, required=False)
    meta = JSONField(required=False)
    answers_data = AnswerSerializer(source="answers", many=True, read_only=True)
    related_question_data = QuestionSerializer(source="related_question", read_only=True)

    class Meta:
        model = SurveyItem
        fields = [
            "related_question", "updated", "answers", "meta", "created", "has_attachments", "type", "survey", "id",
            "sender", "text", "position", "sender_data", "attachments_data", "answers_data", "related_question_data"
        ]
        read_only_fields = [
            "related_question", "updated", "meta", "sender_data", "created", "has_attachments", "type", "survey",
            "sender", "attachments_data", "id", "position"
        ]

    required_fields = [
        "survey", "type", "position"
    ]


class SurveyListCreateSerializer(ModelSerializer):
    automated_sender_data = chat_settings.ACCOUNT_SERIALIZER(source="automated_sender", read_only=True)
    user_data = chat_settings.ACCOUNT_SERIALIZER(source="user", read_only=True)

    def validate_schema(self, schema):
        if schema.type not in chat_settings.SURVEYS_ALLOWED_SCHEMA_TYPES:
            raise serializers.ValidationError(["NOT_ALLOWED"])
        return schema

    class Meta:
        model = Survey
        fields = [
            "schema", "user", "updated", "automated_sender", "id", "created", "automated_sender_data", "user_data",
            "state"
        ]
        read_only_fields = [
            "id", "updated", "created", "user", "state"
        ]

    required_fields = [
        "schema"
    ]
