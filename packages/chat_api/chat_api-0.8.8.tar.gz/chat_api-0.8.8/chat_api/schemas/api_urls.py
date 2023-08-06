# -*- coding: utf-8 -*-
from chat_api.schemas.api import SchemaDetailsAPI, SchemasListAPI
from django.conf.urls import url

urlpatterns = [
    url(r"^schemas/(?P<pk>[\d]+)$", SchemaDetailsAPI.as_view(), name="schema-details"),
    url(r"^schemas/(?P<type>[\w]+)$", SchemasListAPI.as_view(), name="schemas-list"),
]
