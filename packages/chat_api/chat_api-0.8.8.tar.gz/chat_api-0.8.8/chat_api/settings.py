# -*- coding: utf-8 -*-
"""Settings for Chat API are all namespaced in the CHAT_SETTINGS setting.

For example your project's "settings.py" file might look like this:

CHAT_SETTINGS = {
    "TYPES_CHAT": (("chat", "chat"), ("survey", "survey"), ("tracker", "tracker")),

    "PERMISSIONS_ATTACHMENT_OBJECT_BY_MESSAGE_ID": "chat_api.permissions.AttachmentObjectByMessageID",
}

To simplify overriding those settings they have a flat structure.

This module provides the "api_setting" object, that is used to access Chat API settings, checking for user settings
first, then falling back to the defaults.

This code is based on Django Rest Framework's settings.
"""
from __future__ import unicode_literals
from django.conf import settings
from django.test.signals import setting_changed
from rest_framework.settings import perform_import

DEFAULTS = {
    # Serializers
    "ACCOUNT_SERIALIZER": "chat_api.utils.serializers.SimpleAccountSerializer",

    # Schemas
    "TYPES_SCHEMA": (("survey", "Survey"), ("automated_flow", "Automated Flow")),
    "TYPES_SCHEMA_LIST_THROUGH_API": ("survey", "automated_flow"),
    "TYPES_SCHEMA_GET_THROUGH_API": ("survey",),
    "ALLOW_EDIT_PUBLISHED_SCHEMAS": False,

    # Chat
    "TYPES_CHAT": (("chat", "Chat"), ("survey", "Survey"), ("tracker", "Tracker")),
    "TYPES_CHAT_DEFAULT": "chat",
    "TYPES_CHAT_LIST_THROUGH_API": ("chat", "survey", "tracker"),
    "CHAT_MESSAGE_FILTER_QUERYSET": None,  # filter_queryset(queryset, user) : queryset
    "CHAT_MESSAGE_USER_FILTER": None,  # user_filter(message, user) : boolean

    # Surveys
    "SURVEYS_ALLOWED_SCHEMA_TYPES": ("survey", ),

    # Attachments
    "TYPES_CUSTOM_ATTACHMENTS": (),  # ("type", "Label")
    "CUSTOM_ATTACHMENTS_VALIDATION": {},  # "type": "validation_func"
    "CUSTOM_ATTACHMENTS_PRE_SAVE": {},  # "type": "pre_save_func"
    "CUSTOM_ATTACHMENTS_THUMBNAIL_GENERATOR": {},  # "type": "thumbnail_generator"
    "CUSTOM_ATTACHMENTS_GET_SRC": {},  # "type": "get_src"
    "CUSTOM_ATTACHMENTS_GET_THUMBNAIL": {},
    "ATTACHMENT_THUMBNAIL_SIZE": (100, 100),

    # Pagination
    "PAGINATION_THREAD_LIST": "drf_tweaks.pagination.NoCountsLimitOffsetPagination",
    "PAGINATION_MESSAGES_LIST": "drf_tweaks.pagination.NoCountsLimitOffsetPagination",
    "PAGINATION_GLOBAL_SURVEY_LIST": "drf_tweaks.pagination.NoCountsLimitOffsetPagination",
    "PAGINATION_ACCOUNT_SURVEY_LIST": "drf_tweaks.pagination.NoCountsLimitOffsetPagination",

    # Permissions
    # messages: read, create; thread: read
    "THREAD_PERMISSIONS_DEFAULT": 1 | 2 | 16,
    # messages: read, create, delete; thread: read, edit, delete, add user, remove user
    "THREAD_CREATOR_PERMISSIONS_DEFAULT": 1 | 2 | 8 | 16 | 32 | 64 | 128 | 258,
    "PERMISSIONS_ATTACHMENT_OBJECT_BY_MESSAGE_ID": "chat_api.permissions.AttachmentObjectByMessageID",
    "PERMISSIONS_SURVEY_ATTACHMENT_OBJECT_BY_ITEM_ID": "chat_api.permissions.SurveyAttachmentObjectByItemID",
    "PERMISSIONS_THREADS_LIST_BY_USER_ID_AND_TYPE": "chat_api.permissions.ThreadsListByUserIDAndType",
    "PERMISSIONS_THREAD_OBJECT_BY_THREAD_ID": "chat_api.permissions.ThreadObjectByThreadID",
    "PERMISSIONS_THREAD_USERS_LIST_BY_THREAD_ID": "chat_api.permissions.ThreadUsersListByThreadID",
    "PERMISSIONS_THREAD_USERS_OBJECT_BY_THREAD_ID": "chat_api.permissions.ThreadUsersObjectByThreadID",
    "PERMISSIONS_ATTACHMENTS_LIST_BY_MESSAGE_ID": "chat_api.permissions.AttachmentsListByMessageID",
    "PERMISSIONS_SURVEY_ITEM_OBJECT_BY_SURVEY_ID": "chat_api.permissions.SurveyItemObjectBySurveyID",
    "PERMISSIONS_SURVEY_ATTACHMENT_LIST_BY_ITEM_ID": "chat_api.permissions.SurveyAttachmentListByItemID",
    "PERMISSIONS_SURVEY_OBJECT": "chat_api.permissions.SurveyObject",
    "PERMISSIONS_SURVEYS_LIST_BY_USER_ID": "chat_api.permissions.SurveysListByUserID",
    "PERMISSIONS_SURVEY_ITEMS_LIST_BY_SURVEY_ID": "chat_api.permissions.SurveyItemsListBySurveyID",
    "PERMISSIONS_SURVEYS_GLOBAL_LIST": "chat_api.permissions.SurveysGlobalList",
    "PERMISSIONS_MESSAGES_LIST_BY_THREAD_ID": "chat_api.permissions.MessagesListByThreadID",
    "PERMISSIONS_MESSAGE_OBJECT_BY_THREAD_ID": "chat_api.permissions.MessageObjectByThreadID",
    "PERMISSIONS_SCHEMA_OBJECT": "chat_api.permissions.SchemaObject",
    "PERMISSIONS_SCHEMA_LIST_BY_TYPE": "chat_api.permissions.SchemaListByType",
    "PERMISSIONS_THREAD_WS_SUBSCRIBE": "chat_api.permissions.ThreadWSSubscribe",
    "PERMISSIONS_THREAD_ROLLBACK": "chat_api.permissions.ThreadRollback",

    # Search
    "ELASTICSEARCH_URL": None,
    "ELASTICSEARCH_PREFIX": "",

    # optimizations
    "OPTIMIZATIONS_BY_THREAD_TYPE": {
        # "some_thread_type": {
        #     "BULK_CREATE_ON_ADDING_WITH_QUESTION": False,   # not implemented, perhaps later - no ids
        #     "NO_WS_TO_SUBSCRIBED": False,
        #     "NO_UPDATES_FOR_LAST_MESSAGE_AND_UPDATED": False,
        #     "LIMIT_FIELDS_TO": [],
        #     "SEND_SIGNAL_INSTEAD_ADDING_ANSWERS": False,
        #     "NO_MOVE_TO_NEXT_QID": False,
        #     "NOT_INDEXED": False,
        #     "LIMIT_VARIABLES_MODIFICATIONS_TO": None  # ["var1", "var2"] if empty list - non will be applied
        # }
    },
    "OPTIMIZATIONS_BY_SURVEY_TYPE": {
        # "some_survey_type": {
        #     "NO_STATE_UPDATE": True,
        # }
    }
}

# List of settings that may be in string import notation.
IMPORT_STRINGS = (
    # Serializers
    "ACCOUNT_SERIALIZER",

    # Pagination
    "PAGINATION_THREAD_LIST",
    "PAGINATION_MESSAGES_LIST",
    "PAGINATION_GLOBAL_SURVEY_LIST",
    "PAGINATION_ACCOUNT_SURVEY_LIST",

    # Permissions
    "PERMISSIONS_ATTACHMENT_OBJECT_BY_MESSAGE_ID",
    "PERMISSIONS_SURVEY_ATTACHMENT_OBJECT_BY_ITEM_ID",
    "PERMISSIONS_THREADS_LIST_BY_USER_ID_AND_TYPE",
    "PERMISSIONS_THREAD_OBJECT_BY_THREAD_ID",
    "PERMISSIONS_THREAD_USERS_LIST_BY_THREAD_ID",
    "PERMISSIONS_THREAD_USERS_OBJECT_BY_THREAD_ID",
    "PERMISSIONS_ATTACHMENTS_LIST_BY_MESSAGE_ID",
    "PERMISSIONS_SURVEY_ITEM_OBJECT_BY_SURVEY_ID",
    "PERMISSIONS_SURVEY_ATTACHMENT_LIST_BY_ITEM_ID",
    "PERMISSIONS_SURVEY_OBJECT",
    "PERMISSIONS_SURVEYS_LIST_BY_USER_ID",
    "PERMISSIONS_SURVEY_ITEMS_LIST_BY_SURVEY_ID",
    "PERMISSIONS_SURVEYS_GLOBAL_LIST",
    "PERMISSIONS_MESSAGES_LIST_BY_THREAD_ID",
    "PERMISSIONS_MESSAGE_OBJECT_BY_THREAD_ID",
    "PERMISSIONS_SCHEMA_OBJECT",
    "PERMISSIONS_SCHEMA_LIST_BY_TYPE",
    "PERMISSIONS_THREAD_WS_SUBSCRIBE",
    "PERMISSIONS_THREAD_ROLLBACK",

    # Other
    "CHAT_MESSAGE_FILTER_QUERYSET",
    "CHAT_MESSAGE_USER_FILTER"
)


class ChatSettings(object):
    """A settings object, that allows API settings to be accessed as properties.

    For example:
        from chat_api.settings import chat_settings
        print(chat_settings.DEFAULT_RENDERER_CLASSES)

    Any setting with string import paths will be automatically resolved
    and return the class, rather than the string literal.
    """

    def __init__(self, user_settings=None):
        if user_settings:
            self._user_settings = self.__check_user_settings(user_settings)

    @property
    def user_settings(self):
        if not hasattr(self, '_user_settings'):
            self._user_settings = getattr(settings, 'CHAT_SETTINGS', {})
        return self._user_settings

    def __getattr__(self, attr):
        if attr not in DEFAULTS:
            raise AttributeError("Invalid API setting: '%s'" % attr)

        try:  # than user settings
            val = self.user_settings[attr]
        except KeyError:  # fall back to defaults
            val = DEFAULTS[attr]

        # Coerce import strings into classes
        if attr in IMPORT_STRINGS:
            val = perform_import(val, attr)

        # Cache the result
        setattr(self, attr, val)
        return val

    def __check_user_settings(self, user_settings):
        for setting in user_settings:
            if setting not in DEFAULTS:
                raise RuntimeError("The '%s' is incorrect. Please check settings.DEFAULTS for the available options")
        return user_settings


class ChatSettingOutter(object):
    def __init__(self, settings_inner):
        self.settings_inner = settings_inner

    def __getattr__(self, attr):
        return getattr(self.settings_inner, attr)


chat_settings = ChatSettingOutter(ChatSettings())


def reload_api_settings(*args, **kwargs):
    global chat_settings
    setting, value = kwargs['setting'], kwargs['value']
    if setting == 'CHAT_SETTINGS':
        chat_settings.settings_inner = ChatSettings(value)


setting_changed.connect(reload_api_settings)
