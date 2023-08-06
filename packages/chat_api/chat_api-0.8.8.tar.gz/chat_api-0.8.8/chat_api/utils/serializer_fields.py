# -*- coding: utf-8 -*-
from rest_framework.fields import CharField


class JSONField(CharField):
    type_name = 'JSONField'

    def to_internal_value(self, data):
        return data

    def to_representation(self, value):
        return value
