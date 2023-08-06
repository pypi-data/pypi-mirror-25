# -*- coding: utf-8 -*-
from chat_api.schemas.models import Schema
from chat_api.schemas.serializers import SchemaDetailsSerializer, SchemaSerializer
from chat_api.settings import chat_settings
from chat_api.utils.decorators import ClassProperty
from django.db.models import Q
from drf_tweaks.autodoc import autodoc
from drf_tweaks.autofilter import autofilter
from drf_tweaks.optimizator import AutoOptimizeMixin
from rest_framework.generics import ListAPIView, RetrieveAPIView


@autodoc()
class SchemaDetailsAPI(AutoOptimizeMixin, RetrieveAPIView):
    queryset = Schema.objects.all()
    serializer_class = SchemaDetailsSerializer
    pagination_class = None

    @ClassProperty
    def permission_classes(self):
        return (chat_settings.PERMISSIONS_SCHEMA_OBJECT,)


@autodoc()
@autofilter()
class SchemasListAPI(AutoOptimizeMixin, ListAPIView):
    queryset = Schema.objects.all()
    serializer_class = SchemaSerializer
    pagination_class = None

    @ClassProperty
    def permission_classes(self):
        return (chat_settings.PERMISSIONS_SCHEMA_LIST_BY_TYPE,)

    def get_queryset(self):
        queryset = super(SchemasListAPI, self).get_queryset()
        queryset = queryset.filter(
            Q(type=self.kwargs["type"])
        )
        return queryset
