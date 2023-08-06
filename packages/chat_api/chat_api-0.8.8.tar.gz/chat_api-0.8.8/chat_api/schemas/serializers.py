# -*- coding: utf-8 -*-
from chat_api.common import AttachmentSerializerMixin
from chat_api.schemas.models import Answer, AttachmentTemplate, Group, Question, Schema
from chat_api.utils.serializer_fields import JSONField
from drf_tweaks.serializers import ModelSerializer
from rest_framework import serializers


class AnswerSerializer(ModelSerializer):
    meta = JSONField(required=False)
    variable_modifications = JSONField(read_only=True)

    class Meta:
        model = Answer
        fields = [
            "question", "next_qid", "meta", "id", "text", "position", "variable_modifications", "exclusive"
        ]
        read_only_fields = [
            "id", "variable_modifications", "exclusive"
        ]

    required_fields = [
        "question", "next_qid", "position", "text"
    ]


class AttachmentTemplateSerializer(AttachmentSerializerMixin, ModelSerializer):
    options = JSONField(required=False)
    thumbnail = JSONField(required=False, read_only=True)
    src = serializers.SerializerMethodField()

    class Meta:
        model = AttachmentTemplate
        fields = [
            "question", "title", "type", "description", "src", "id", "thumbnail", "options", "object_id", "content_type"
        ]
        read_only_fields = [
            "id"
        ]

    required_fields = [
        "type"
    ]


class QuestionSerializer(ModelSerializer):
    answers = AnswerSerializer(read_only=True, required=False, many=True)
    attachments = AttachmentTemplateSerializer(read_only=True, required=False, many=True)
    meta = JSONField(required=False)
    variable_modifications = JSONField(read_only=True)
    forking_rules = JSONField(read_only=True)

    class Meta:
        model = Question
        fields = [
            "schema", "range_to", "next_qid", "meta", "required", "has_attachments", "qid", "choice_open", "type",
            "group", "id", "text", "range_from", "position", "answers", "attachments", "variable_modifications",
            "forking_rules", "show_as_type"
        ]
        read_only_fields = [
            "answers", "has_attachments", "attachments", "id", "variable_modifications", "forking_rules", "show_as_type"
        ]

    required_fields = [
        "schema", "type", "position", "qid", "text"
    ]


class GroupSerializer(ModelSerializer):
    questions = QuestionSerializer(read_only=True, required=False, many=True)

    class Meta:
        model = Group
        fields = [
            "id", "schema", "position", "name", "questions"
        ]
        read_only_fields = [
            "id", "questions"
        ]

    required_fields = [
        "schema", "name", "position"
    ]


class SchemaDetailsSerializer(ModelSerializer):
    groups = GroupSerializer(read_only=True, required=False, many=True)
    questions = QuestionSerializer(source="not_grouped_questions", read_only=True, required=False, many=True)

    class Meta:
        model = Schema
        fields = [
            "name", "published", "version", "type", "deprecated", "id", "groups", "questions"
        ]
        read_only_fields = [
            "id", "version", "deprecated", "questions", "groups"
        ]

    required_fields = [
        "name", "version", "deprecated", "published"
    ]


class SchemaSerializer(ModelSerializer):
    class Meta:
        model = Schema
        fields = [
            "name", "published", "version", "type", "deprecated", "id"
        ]
        read_only_fields = [
            "id", "version", "deprecated"
        ]

    required_fields = [
        "name", "version", "deprecated", "published"
    ]
