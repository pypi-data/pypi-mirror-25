# -*- coding: utf-8 -*-
from chat_api.settings import chat_settings
from chat_api.surveys.models import Survey, SurveyAttachment, SurveyItem
from chat_api.surveys.serializers import (SurveyAttachmentSerializer, SurveyItemListCreateSerializer,
                                          SurveyItemSerializer, SurveyListCreateSerializer, SurveySerializer)
from chat_api.utils.decorators import ClassProperty
from django.db.models import Q
from drf_tweaks.autodoc import autodoc
from drf_tweaks.autofilter import autofilter
from drf_tweaks.optimizator import AutoOptimizeMixin
from rest_framework.generics import ListAPIView, ListCreateAPIView, RetrieveUpdateDestroyAPIView


@autodoc()
@autofilter()
class AccountSurveysListAPI(AutoOptimizeMixin, ListCreateAPIView):
    queryset = Survey.objects.all()
    serializer_class = SurveyListCreateSerializer
    pagination_class = chat_settings.PAGINATION_ACCOUNT_SURVEY_LIST

    @ClassProperty
    def permission_classes(self):
        return (chat_settings.PERMISSIONS_SURVEYS_LIST_BY_USER_ID,)

    def get_queryset(self):
        queryset = super(AccountSurveysListAPI, self).get_queryset()
        queryset = queryset.filter(
            Q(user_id=self.kwargs["user_id"])
        )
        return queryset

    def perform_create(self, serializer):
        serializer.save(user_id=int(self.kwargs["user_id"]))


@autodoc()
class SurveyDetailsAPI(AutoOptimizeMixin, RetrieveUpdateDestroyAPIView):
    queryset = Survey.objects.all()
    serializer_class = SurveySerializer
    pagination_class = None

    @ClassProperty
    def permission_classes(self):
        return (chat_settings.PERMISSIONS_SURVEY_OBJECT,)


@autodoc()
@autofilter()
class SurveyItemsListAPI(AutoOptimizeMixin, ListCreateAPIView):
    queryset = SurveyItem.objects.select_related("related_question").all()
    serializer_class = SurveyItemListCreateSerializer
    pagination_class = None

    @ClassProperty
    def permission_classes(self):
        return (chat_settings.PERMISSIONS_SURVEY_ITEMS_LIST_BY_SURVEY_ID,)

    def get_queryset(self):
        queryset = super(SurveyItemsListAPI, self).get_queryset()
        queryset = queryset.filter(
            Q(survey_id=self.kwargs["survey_id"])
        )
        return queryset

    def perform_create(self, serializer):
        serializer.save(
            sender=self.request.user,
            survey_id=self.kwargs["survey_id"],
            position=serializer.validated_data["related_question"].position
        )


@autodoc()
@autofilter()
class SurveyItemAttachmentsListAPI(AutoOptimizeMixin, ListCreateAPIView):
    queryset = SurveyAttachment.objects.all()
    serializer_class = SurveyAttachmentSerializer
    pagination_class = None

    @ClassProperty
    def permission_classes(self):
        return (chat_settings.PERMISSIONS_SURVEY_ATTACHMENT_LIST_BY_ITEM_ID,)

    def get_queryset(self):
        queryset = super(SurveyItemAttachmentsListAPI, self).get_queryset()
        queryset = queryset.filter(
            Q(item_id=self.kwargs["item_id"])
        )
        return queryset

    def perform_create(self, serializer):
        serializer.save(item_id=int(self.kwargs["item_id"]))


@autodoc()
class SurveyItemAttachmentDetailsAPI(AutoOptimizeMixin, RetrieveUpdateDestroyAPIView):
    queryset = SurveyAttachment.objects.all()
    serializer_class = SurveyAttachmentSerializer
    pagination_class = None

    @ClassProperty
    def permission_classes(self):
        return (chat_settings.PERMISSIONS_SURVEY_ATTACHMENT_OBJECT_BY_ITEM_ID,)

    def get_queryset(self):
        queryset = super(SurveyItemAttachmentDetailsAPI, self).get_queryset()
        queryset = queryset.filter(
            Q(item_id=self.kwargs["item_id"])
        )
        return queryset


@autodoc()
class SurveyItemDetailsAPI(AutoOptimizeMixin, RetrieveUpdateDestroyAPIView):
    queryset = SurveyItem.objects.select_related("related_question").all()
    serializer_class = SurveyItemSerializer
    pagination_class = None

    @ClassProperty
    def permission_classes(self):
        return (chat_settings.PERMISSIONS_SURVEY_ITEM_OBJECT_BY_SURVEY_ID,)

    def get_queryset(self):
        queryset = super(SurveyItemDetailsAPI, self).get_queryset()
        queryset = queryset.filter(
            Q(survey_id=self.kwargs["survey_id"])
        )
        return queryset


@autodoc()
@autofilter()
class SurveysListAPI(AutoOptimizeMixin, ListAPIView):
    queryset = Survey.objects.all()
    serializer_class = SurveyListCreateSerializer
    pagination_class = chat_settings.PAGINATION_GLOBAL_SURVEY_LIST

    @ClassProperty
    def permission_classes(self):
        return (chat_settings.PERMISSIONS_SURVEYS_GLOBAL_LIST,)
