# -*- coding: utf-8 -*-
from chat_api.chat.api import (AccountThreadsListAPI, ThreadDetailsAPI, ThreadMessageAttachmentDetailsAPI,
                               ThreadMessageAttachmentsListAPI, ThreadMessageDetailsAPI, ThreadMessagesListAPI,
                               ThreadRollbackAPI, ThreadUsersAPI, ThreadUsersDetailsAPI, ThreadWSSubscribeAPI)
from django.conf.urls import url

urlpatterns = [
    url(r"^accounts/(?P<user_id>[\d]+)/threads/(?P<type>[\w]+)$", AccountThreadsListAPI.as_view(),
        name="account-threads-list"),
    url(r"^threads/(?P<thread_id>[\d]+)$", ThreadDetailsAPI.as_view(), name="thread-details"),
    url(r"^threads/(?P<thread_id>[\d]+)/rollback$", ThreadRollbackAPI.as_view(), name="thread-rollback"),
    url(r"^threads/(?P<thread_id>[\d]+)/users$", ThreadUsersAPI.as_view(), name="thread-users"),
    url(r"^threads/(?P<thread_id>[\d]+)/users/(?P<user_id>[\d]+)$", ThreadUsersDetailsAPI.as_view(),
        name="thread-users-details"),
    url(r"^threads/(?P<thread_id>[\d]+)/messages$", ThreadMessagesListAPI.as_view(), name="thread-messages-list"),
    url(r"^threads/(?P<thread_id>[\d]+)/messages/(?P<message_id>[\d]+)/attachments$",
        ThreadMessageAttachmentsListAPI.as_view(), name="thread-message-attachments-list"),
    url(r"^threads/(?P<thread_id>[\d]+)/messages/(?P<message_id>[\d]+)/attachments/(?P<pk>[\d]+)$",
        ThreadMessageAttachmentDetailsAPI.as_view(), name="thread-message-attachment-details"),
    url(r"^threads/(?P<thread_id>[\d]+)/messages/(?P<pk>[\d]+)$", ThreadMessageDetailsAPI.as_view(),
        name="thread-message-details"),
    url(r"^threads/(?P<thread_id>[\d]+)/ws-subscribe$", ThreadWSSubscribeAPI.as_view(), name="thread-ws-subscribe"),
]
