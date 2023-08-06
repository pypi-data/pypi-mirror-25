# -*- coding: utf-8 -*-
from chat_api.chat.models import Attachment, Message, UnreadMessage, UserThread
from chat_api.management.commands.dump_schema import Command
from chat_api.management.commands.load_schema import FixtureLoader
from chat_api.schemas.models import Answer, AttachmentTemplate, Group, Question, Schema
from chat_api.schemas.utils import SchemaChecker
from chat_api.settings import chat_settings
from chat_api.surveys.models import Survey, SurveyAttachment, SurveyItem
from django import forms
from django.contrib import admin, messages
from django.http import HttpResponse
from django.utils.translation import ugettext_lazy as _
from io import StringIO


# chat
class UserThreadAdmin(admin.ModelAdmin):
    list_display = (
        "id", "user", "thread", "type", "state", "schema", "repeat_until", "next_restart", "created", "updated"
    )
    list_filter = ("type",)
    readonly_fields = (
        "automated_sender", "created", "frequency_unit", "frequency_value", "initial_question", "next_restart",
        "notifications", "on_finish", "permissions", "question", "related_message", "repeat_until", "schema", "state",
        "thread", "type", "updated", "user", "last_message", "variables_pool"
    )

    def has_add_permission(self, request, obj=None):
        return False


class AttachmentInline(admin.TabularInline):
    model = Attachment
    extra = 0


class UnreadMessageInline(admin.TabularInline):
    model = UnreadMessage
    extra = 0


class MessageAdmin(admin.ModelAdmin):
    inlines = [AttachmentInline, UnreadMessageInline]
    list_display = ("id", "thread", "type", "created", "updated", "sender", "text")


# surveys
class SurveyAdmin(admin.ModelAdmin):
    list_display = (
        "id", "created", "updated", "user", "schema", "state"
    )
    readonly_fields = (
        "automated_sender", "created", "schema", "updated", "user", "state"
    )


class SurveyAttachmentInline(admin.TabularInline):
    model = SurveyAttachment
    extra = 0


class SurveyItemAdmin(admin.ModelAdmin):
    inlines = [SurveyAttachmentInline]
    list_display = ("id", "survey", "type", "created", "updated")


# schemas
class AttachmentTemplateInline(admin.TabularInline):
    model = AttachmentTemplate
    extra = 0

    def get_readonly_fields(self, request, obj):
        readonly_fields = super(AttachmentTemplateInline, self).get_readonly_fields(request, obj)
        if obj and obj.schema_id and obj.schema.published and not chat_settings.ALLOW_EDIT_PUBLISHED_SCHEMAS:
            return readonly_fields + ("description", "object_id", "content_type", "options", "file", "url", "thumbnail",
                                      "thumbnail_image", "title", "type")
        return readonly_fields

    def get_formset(self, request, obj=None, **kwargs):
        if obj and obj.schema_id and obj.schema.published and not chat_settings.ALLOW_EDIT_PUBLISHED_SCHEMAS:
            kwargs['extra'] = 0
            kwargs['max_num'] = 0
        return super(AttachmentTemplateInline, self).get_formset(request, obj, **kwargs)

    def has_delete_permission(self, request, obj=None):
        if not chat_settings.ALLOW_EDIT_PUBLISHED_SCHEMAS:
            if not obj or obj and obj.schema_id and obj.schema.published:
                return False
        return True


class AnswerInline(admin.TabularInline):
    model = Answer
    extra = 0

    def get_readonly_fields(self, request, obj):
        readonly_fields = super(AnswerInline, self).get_readonly_fields(request, obj)
        if obj and obj.schema_id and obj.schema.published and not chat_settings.ALLOW_EDIT_PUBLISHED_SCHEMAS:
            return readonly_fields + ("meta", "next_qid", "position", "text", "variable_modifications", "exclusive")
        return readonly_fields

    def get_formset(self, request, obj=None, **kwargs):
        if obj and obj.schema_id and obj.schema.published and not chat_settings.ALLOW_EDIT_PUBLISHED_SCHEMAS:
            kwargs['extra'] = 0
            kwargs['max_num'] = 0
        return super(AnswerInline, self).get_formset(request, obj, **kwargs)

    def has_delete_permission(self, request, obj=None):
        if not chat_settings.ALLOW_EDIT_PUBLISHED_SCHEMAS:
            if not obj or obj and obj.schema_id and obj.schema.published:
                return False
        return True


class QuestionAdmin(admin.ModelAdmin):
    inlines = [AnswerInline, AttachmentTemplateInline]
    model = Question
    extra = 0
    readonly_fields = ("has_attachments", )
    list_display = ("schema", "text", "type", "position", "qid", "next_qid", "answers_next_qid_list", "group")
    list_filter = ("schema", "group", "type")

    def get_readonly_fields(self, request, obj):
        readonly_fields = super(QuestionAdmin, self).get_readonly_fields(request, obj)
        if obj and obj.schema_id and obj.schema.published and not chat_settings.ALLOW_EDIT_PUBLISHED_SCHEMAS:
            return readonly_fields + ("choice_open", "group", "meta", "next_qid", "position", "qid", "range_from",
                                      "range_to", "required", "text", "type", "schema", "variable_modifications",
                                      "forking_rules", "show_as_type")
        return readonly_fields

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        try:
            if obj and obj.schema:
                form.base_fields["group"].queryset = form.base_fields["group"].queryset.filter(schema=obj.schema)
            elif not obj and "group" in form.base_fields:
                # hide this field on object creation
                del form.base_fields["group"]
        except KeyError:
            # happens when question is read only
            pass

        return form

    def get_formset(self, request, obj=None, **kwargs):
        if obj and obj.published and not chat_settings.ALLOW_EDIT_PUBLISHED_SCHEMAS:
            kwargs['extra'] = 0
            kwargs['max_num'] = 0
        formset = super(QuestionAdmin, self).get_formset(request, obj, **kwargs)

        if "group" in formset.form.base_fields:
            group = formset.form.base_fields["group"]
            if obj:
                group.queryset = group.queryset.filter(schema=obj)
            else:
                group.queryset = group.queryset.none()

        return formset

    def has_delete_permission(self, request, obj=None):
        if not chat_settings.ALLOW_EDIT_PUBLISHED_SCHEMAS:
            if not obj or obj and obj.schema_id and obj.schema.published:
                return False
        return True


class GroupInline(admin.TabularInline):
    model = Group
    extra = 3

    def get_readonly_fields(self, request, obj):
        readonly_fields = super(GroupInline, self).get_readonly_fields(request, obj)
        if obj and obj.published and not chat_settings.ALLOW_EDIT_PUBLISHED_SCHEMAS:
            return readonly_fields + ("name", "position")
        return readonly_fields

    def get_formset(self, request, obj=None, **kwargs):
        if obj and obj.published and not chat_settings.ALLOW_EDIT_PUBLISHED_SCHEMAS:
            kwargs['extra'] = 0
            kwargs['max_num'] = 0
        return super(GroupInline, self).get_formset(request, obj, **kwargs)

    def has_delete_permission(self, request, obj=None):
        if not chat_settings.ALLOW_EDIT_PUBLISHED_SCHEMAS:
            if not obj or obj and obj.published:
                return False
        return True


class SchemaCreateForm(forms.ModelForm):
    name = forms.CharField(required=False)
    type = forms.ChoiceField(required=False, choices=chat_settings.TYPES_SCHEMA)
    schema_file = forms.FileField(required=False)

    def clean(self):
        schema_file = self.cleaned_data.get("schema_file", None)
        name = self.cleaned_data.get("name", None)
        type = self.cleaned_data.get("type", None)
        errors = {}
        if not name and not schema_file:
            errors["name"] = "This field is required when you're not uploading schema from file"
        if not type and not schema_file:
            errors["type"] = "This field is required when you're not uploading schema from file"
        if errors:
            raise forms.ValidationError(errors)
        return self.cleaned_data

    def clean_schema_file(self):
        schema_file = self.cleaned_data.get("schema_file", None)
        if self.instance.pk and schema_file:
            raise forms.ValidationError("Schema file may be specified only on creation")
        return schema_file

    def save(self, commit=True):
        schema_file = self.cleaned_data.get("schema_file", None)
        if schema_file:
            FixtureLoader(fixture=schema_file).run()
            return Schema.objects.order_by("-id").first()
        else:
            return super(SchemaCreateForm, self).save(commit)

    class Meta:
        model = Schema
        fields = ("name", "type", "published", "deprecated", "version")


class SchemaAdmin(admin.ModelAdmin):
    inlines = [GroupInline]
    list_display = ("id", "name", "published", "deprecated", "type", "version")
    readonly_fields = ("published", "deprecated", "version")
    actions = ("delete_action", "publish_action", "copy_as_unpublished_action", "download_schema", "verify_schema")
    list_filter = ("name", "published", "deprecated", "type")

    def save_related(self, request, form, formsets, change):
        for formset in formsets:
            self.save_formset(request, form, formset, change=change)

    def get_actions(self, request):
        actions_dict = super(SchemaAdmin, self).get_actions(request)
        if "delete_selected" in actions_dict:
            del actions_dict["delete_selected"]
        return actions_dict

    def get_readonly_fields(self, request, obj=None):
        """Do not allow editing of published fields."""
        if obj and obj.published and not chat_settings.ALLOW_EDIT_PUBLISHED_SCHEMAS:
            return self.readonly_fields + ("name", "type")
        return self.readonly_fields

    def delete_action(self, request, queryset):
        for schema in queryset:
            if not schema.published:
                schema.delete()
    delete_action.short_description = _("Delete selected not published schemas")

    def publish_action(self, request, queryset):
        for schema in queryset:
            schema.publish()
    publish_action.short_description = _("Publish selected schemas")

    def copy_as_unpublished_action(self, request, queryset):
        for schema in queryset:
            schema.copy_as_unpublished()
    copy_as_unpublished_action.short_description = _("Copy schema as unpublished so it may be edited")

    def download_schema(self, request, queryset):
        for schema in queryset:
            output = StringIO()
            Command.dump_schema(schema, output)

            output.seek(0)
            response = HttpResponse(output, content_type="text/csv")
            response["Content-Disposition"] = "attachment; filename={name}-{pk}.json".format(
                name=schema.name, pk=schema.pk
            )
            return response  # downloading max 1 schema
    download_schema.short_description = _("Download one schema")

    def verify_schema(self, request, queryset):
        for schema in queryset:
            schema_checker = SchemaChecker(schema)
            if not schema_checker.run():
                for error in schema_checker.errors:
                    messages.error(request, error)
            break  # veryfiyng max one schema
    verify_schema.short_description = _("Verify one schema")

    def get_form(self, request, obj=None, **kwargs):
        if obj is None:
            self.form = SchemaCreateForm

        return super(SchemaAdmin, self).get_form(request, obj, **kwargs)

    def has_delete_permission(self, request, obj=None):
        if not obj and not chat_settings.ALLOW_EDIT_PUBLISHED_SCHEMAS or obj and obj.published:
            return False
        return True


admin.site.register(UserThread, UserThreadAdmin)
admin.site.register(Message, MessageAdmin)
admin.site.register(Survey, SurveyAdmin)
admin.site.register(SurveyItem, SurveyItemAdmin)
admin.site.register(Schema, SchemaAdmin)
admin.site.register(Question, QuestionAdmin)
