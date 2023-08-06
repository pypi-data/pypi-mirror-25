# -*- coding: utf-8 -*-
from django.conf.urls import include, url
from rest_framework.routers import DefaultRouter

urlpatterns = [
    url(r"^", include("chat_api.chat.api_urls")),
    url(r"^", include("chat_api.schemas.api_urls")),
    url(r"^", include("chat_api.surveys.api_urls")),
]

router = DefaultRouter()
urlpatterns += router.urls
