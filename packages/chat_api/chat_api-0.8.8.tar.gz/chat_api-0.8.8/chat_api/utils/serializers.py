# -*- coding: utf-8 -*-
from drf_tweaks.serializers import Serializer
from rest_framework import serializers


class SimpleAccountSerializer(Serializer):
    first_name = serializers.SerializerMethodField()
    last_name = serializers.SerializerMethodField()
    id = serializers.SerializerMethodField()
    avatar = serializers.SerializerMethodField()

    def get_first_name(self, obj):
        return getattr(obj, "first_name", "First")

    def get_last_name(self, obj):
        return getattr(obj, "last_name", "Last")

    def get_id(self, obj):
        return getattr(obj, "id", "0")

    def get_avatar(self, obj):
        if hasattr(obj, "avatar"):
            return obj.avatar.url
        return "https://www.gravatar.com/avatar/205e460b479e2e5b48aec07710c08d50"
