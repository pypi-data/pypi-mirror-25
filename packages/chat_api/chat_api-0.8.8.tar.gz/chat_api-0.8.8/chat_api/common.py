# -*- coding: utf-8 -*-
from chat_api.settings import chat_settings
from django.conf import settings
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from io import BytesIO
from PIL import Image
from rest_framework import serializers
from rest_framework.settings import perform_import
from six import string_types

import base64
import magic
import uuid


class AttachmentTypes(object):
    TYPE_IMAGE = "image"
    TYPE_YOUTUBE = "youtube"
    TYPE_OBJECT_REFERENCE = "object_reference"
    TYPE_CHOICES = (
        (TYPE_IMAGE, "Image"),
        (TYPE_YOUTUBE, "Youtube"),
        (TYPE_OBJECT_REFERENCE, "Object Reference")
    ) + chat_settings.TYPES_CUSTOM_ATTACHMENTS


class AttachmentSerializerMixin(object):
    @classmethod
    def _get_func(cls, setting_dict, type_key):
        """ gets function based on settings - with replacing string with func, to not reload each time """
        func = setting_dict.get(type_key, None)
        if func is not None and isinstance(func, string_types):
            func = perform_import(func, type_key)
            setting_dict[type_key] = func
        return func

    def get_type(self, data):
        if self.instance:
            return self.instance.type
        return data.get("type", "incorrect")

    def validate(self, data):
        attachment_type = self.get_type(data)

        errors = {}
        if attachment_type == AttachmentTypes.TYPE_IMAGE:
            if "file_content" not in data:
                errors["file_content"] = ["REQUIRED"]
            else:
                file_content = base64.b64decode(data["file_content"])
                mime = magic.from_buffer(file_content, mime=True)
                if mime not in settings.ACCEPTED_IMAGE_MIME:
                    raise serializers.ValidationError(["INCORRECT_TYPE"])
                self.file_content_mime_value = mime
                self.file_content_data = file_content

        elif attachment_type == AttachmentTypes.TYPE_YOUTUBE:
            if "url" not in data:
                errors["url"] = ["REQUIRED"]
        elif attachment_type == AttachmentTypes.TYPE_OBJECT_REFERENCE:
            for key in ("object_id", "content_type"):
                if key not in data:
                    errors[key] = ["REQUIRED"]
        elif attachment_type == "incorrect":
            errors["type"] = ["REQUIRED"]
        else:
            validate_func = self._get_func(chat_settings.CUSTOM_ATTACHMENTS_VALIDATION, attachment_type)
            if validate_func is not None:
                errors = validate_func(data)

        if errors:
            raise serializers.ValidationError(errors)
        return data

    def generate_thumbnail(self, validated_data):
        attachment_type = self.get_type(validated_data)

        if attachment_type == AttachmentTypes.TYPE_IMAGE:
            if "file" in validated_data and getattr(self, "file_content_data", None):
                byte_file = BytesIO(self.file_content_data)
                byte_file.seek(0)
                image = Image.open(byte_file)
                image.thumbnail(chat_settings.ATTACHMENT_THUMBNAIL_SIZE, Image.ANTIALIAS)

                image_type = settings.MIME_TO_EXT[self.file_content_mime_value]
                if image_type == "jpg":
                    image_type = "jpeg"
                temp_handle = BytesIO()
                image.save(temp_handle, image_type)
                temp_handle.seek(0)

                path = default_storage.save(
                    "attachments/thumbnails/%s.%s" % (
                        str(base64.urlsafe_b64encode(uuid.uuid4().bytes).decode().replace("=", "")),
                        settings.MIME_TO_EXT[self.file_content_mime_value]
                    ),
                    ContentFile(temp_handle.getvalue())
                )
                validated_data["thumbnail_image"] = path
        elif attachment_type == AttachmentTypes.TYPE_YOUTUBE:
            pass  # TODO
        else:
            thumbnail_generator_func = self._get_func(chat_settings.CUSTOM_ATTACHMENTS_THUMBNAIL_GENERATOR,
                                                      attachment_type)
            if thumbnail_generator_func is not None:
                return thumbnail_generator_func(validated_data)

        return validated_data

    def pre_save(self, validated_data):
        attachment_type = self.get_type(validated_data)

        if attachment_type == AttachmentTypes.TYPE_IMAGE:
            if "file_content" not in validated_data:
                return validated_data

            if validated_data["file_content"]:
                file_content = validated_data.pop("file_content")
                if file_content and hasattr(self, "file_content_data"):
                    path = default_storage.save(
                        "attachments/%s.%s" % (
                            str(base64.urlsafe_b64encode(uuid.uuid4().bytes).decode().replace("=", "")),
                            settings.MIME_TO_EXT[self.file_content_mime_value]
                        ),
                        ContentFile(self.file_content_data)
                    )
                    validated_data["file"] = path
            else:
                validated_data["file"] = ""

        else:
            pre_save_func = self._get_func(chat_settings.CUSTOM_ATTACHMENTS_PRE_SAVE, attachment_type)
            if pre_save_func is not None:
                return pre_save_func(validated_data)

        return validated_data

    def get_src(self, obj):
        if obj.type == AttachmentTypes.TYPE_IMAGE:
            return obj.file.url
        elif obj.type == AttachmentTypes.TYPE_YOUTUBE:
            return obj.url
        else:
            get_src_func = self._get_func(chat_settings.CUSTOM_ATTACHMENTS_GET_SRC, obj.type)
            if get_src_func is not None:
                return get_src_func(obj)
        return ""

    def get_thumbnail(self, obj):
        if obj.type == AttachmentTypes.TYPE_IMAGE:
            return {
                "width": chat_settings.ATTACHMENT_THUMBNAIL_SIZE[0],
                "height": chat_settings.ATTACHMENT_THUMBNAIL_SIZE[1],
                "src": obj.thumbnail_image.url
            }
        else:
            get_src_func = self._get_func(chat_settings.CUSTOM_ATTACHMENTS_GET_THUMBNAIL, obj.type)
            if get_src_func is not None:
                return get_src_func(obj)
        return obj.thumbnail
