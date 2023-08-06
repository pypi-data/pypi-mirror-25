# -*- coding: utf-8 -*-
from chat_api.settings import chat_settings


def get_survey_optimization_option(survey_type, option):
    if survey_type in chat_settings.OPTIMIZATIONS_BY_SURVEY_TYPE:
        return chat_settings.OPTIMIZATIONS_BY_SURVEY_TYPE[survey_type].get(option, None)
    return None
