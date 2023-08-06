# -*- coding: utf-8 -*-
import django.dispatch

chat_api_thread_schema_completed = django.dispatch.Signal(providing_args=["user_thread"])
chosen_answers_signal = django.dispatch.Signal(providing_args=["message", "answers"])
thread_state_changed = django.dispatch.Signal(providing_args=["thread", "state", "previous_state", "user"])
