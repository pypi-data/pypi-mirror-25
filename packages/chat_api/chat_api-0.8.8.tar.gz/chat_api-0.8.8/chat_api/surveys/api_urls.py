# -*- coding: utf-8 -*-
from chat_api.surveys.api import (AccountSurveysListAPI, SurveyDetailsAPI, SurveyItemAttachmentDetailsAPI,
                                  SurveyItemAttachmentsListAPI, SurveyItemDetailsAPI, SurveyItemsListAPI,
                                  SurveysListAPI)
from django.conf.urls import url

urlpatterns = [
    url(r"^accounts/(?P<user_id>[\d]+)/surveys$", AccountSurveysListAPI.as_view(), name="account-surveys-list"),
    url(r"^surveys/(?P<pk>[\d]+)$", SurveyDetailsAPI.as_view(), name="survey-details"),
    url(r"^surveys/(?P<survey_id>[\d]+)/items$", SurveyItemsListAPI.as_view(), name="survey-items-list"),
    url(r"^surveys/(?P<survey_id>[\d]+)/items/(?P<item_id>[\d]+)/attachments$", SurveyItemAttachmentsListAPI.as_view(),
        name="survey-item-attachments-list"),
    url(r"^surveys/(?P<survey_id>[\d]+)/items/(?P<item_id>[\d]+)/attachments/(?P<pk>[\d]+)$",
        SurveyItemAttachmentDetailsAPI.as_view(), name="survey-item-attachment-details"),
    url(r"^surveys/(?P<survey_id>[\d]+)/items/(?P<pk>[\d]+)$", SurveyItemDetailsAPI.as_view(),
        name="survey-item-details"),
    url(r"^surveys$", SurveysListAPI.as_view(), name="surveys-list"),
]
