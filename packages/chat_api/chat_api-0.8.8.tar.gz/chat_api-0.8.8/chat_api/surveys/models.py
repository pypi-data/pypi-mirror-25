# -*- coding: utf-8 -*-
from chat_api.common import AttachmentTypes
from chat_api.surveys.optimizations import get_survey_optimization_option
from chat_api.utils.fields import JSONField
from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey
from django.db import models
from django.db.models.signals import m2m_changed, post_delete, post_save, pre_save

AUTH_USER_MODEL = getattr(settings, 'AUTH_USER_MODEL', 'auth.User')


class Survey(models.Model):
    automated_sender = models.ForeignKey(AUTH_USER_MODEL, null=True, blank=True, db_index=False,
                                         related_name="automated_surveys_sent_by", on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True, db_index=True)
    schema = models.ForeignKey("chat_api.Schema", on_delete=models.CASCADE, db_index=False)
    updated = models.DateTimeField(auto_now=True, db_index=True)
    user = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE)
    state = JSONField(null=True, blank=True)

    def __str__(self):
        return "Survey: %d" % self.pk

    @classmethod
    def _visibility_walk(cls, qid, references, items_map, visible_questions_set):
        if qid not in visible_questions_set and qid >= 0:
            visible_questions_set.add(qid)
            if references[qid] and references[qid] > 0:
                cls._visibility_walk(references[qid], references, items_map, visible_questions_set)

            if qid in items_map:
                for answer in items_map[qid].answers_cache:
                    cls._visibility_walk(answer.next_qid, references, items_map, visible_questions_set)

    def update_state(self, commit=True):
        if get_survey_optimization_option(self.schema.type, "NO_STATE_UPDATE"):
            return
        visible_questions_set = set()
        required_set = set()

        references = {}
        entry_point = None
        for question in self.schema.questions.all():
            if entry_point is None or entry_point.position > question.position:
                entry_point = question
            references[question.qid] = question.next_qid
            if question.required:
                required_set.add(question.qid)

        if not entry_point:
            return  # nothing to see here

        # add items (based on their visibility)
        survey_items = list(self.survey_items.select_related("related_question").all())
        items_map = {}
        answered_set = set()
        for item in survey_items:
            item.answers_cache = []
            items_map[item.related_question.qid] = item
            answered_set.add(item.related_question.qid)

        # mapping answers
        qs = SurveyItem.answers.through.objects.select_related(
            "answer", "answer__question"
        ).filter(surveyitem__in=survey_items)
        for answer_through in qs:
            items_map[answer_through.answer.question.qid].answers_cache.append(answer_through.answer)

        # start from entry point
        self._visibility_walk(entry_point.qid, references, items_map, visible_questions_set)

        # map to list & save
        self.state = {
            "visibility": list(visible_questions_set),
            "completed": answered_set >= required_set & visible_questions_set
        }

        if commit:
            self.save()

    class Meta:
        app_label = "chat_api"


class SurveyItem(models.Model):
    answers = models.ManyToManyField("chat_api.Answer", blank=True, related_name="survey_items")
    created = models.DateTimeField(auto_now_add=True)
    has_attachments = models.BooleanField(default=False)
    meta = JSONField(null=True, blank=True)
    position = models.IntegerField(db_index=True)
    related_question = models.ForeignKey("chat_api.Question", on_delete=models.CASCADE)
    sender = models.ForeignKey(AUTH_USER_MODEL, null=True, blank=True, on_delete=models.CASCADE, db_index=False)
    survey = models.ForeignKey("chat_api.Survey", on_delete=models.CASCADE, related_name="survey_items")
    text = models.TextField(blank=True)
    type = models.CharField(max_length=50, default="answer")
    updated = models.DateTimeField(auto_now=True, db_index=True)

    class Meta:
        app_label = "chat_api"
        unique_together = (("related_question", "survey"),)


class SurveyAttachment(models.Model):
    description = models.TextField(blank=True)
    item = models.ForeignKey("chat_api.SurveyItem", on_delete=models.CASCADE, related_name="attachments")
    object_id = models.PositiveIntegerField(null=True, blank=True)
    content_type = models.ForeignKey("contenttypes.ContentType", null=True, db_index=False, on_delete=models.CASCADE)
    options = JSONField(null=True, blank=True)
    file = models.FileField(null=True, blank=True)
    url = models.URLField(null=True, blank=True)
    thumbnail = JSONField(null=True, blank=True)
    thumbnail_image = models.ImageField(null=True, blank=True)
    title = models.CharField(max_length=255, blank=True)
    type = models.CharField(max_length=50, choices=AttachmentTypes.TYPE_CHOICES)
    content_object = GenericForeignKey("content_type", "object_id")

    class Meta:
        app_label = "chat_api"


def survey_pre_save(sender, instance, **kwargs):
    if not instance.pk:
        instance.update_state(commit=False)


def survey_item_post_save(sender, instance, **kwargs):
    instance.survey.update_state()


def survey_item_post_delete(sender, instance, **kwargs):
    instance.survey.update_state()


def survey_item_m2m_changed(sender, instance, action, **kwargs):
    if action in ("post_add", "post_remove", "post_clear"):
        instance.survey.update_state()


def attachment_post_save(sender, instance, created, **kwargs):
    if created:
        SurveyItem.objects.filter(pk=instance.item_id).update(has_attachments=True)


def attachment_post_delete(sender, instance, **kwargs):
    SurveyItem.objects.filter(pk=instance.item_id).update(
        has_attachments=bool(SurveyAttachment.objects.filter(item_id=instance.item_id).exists())
    )


pre_save.connect(survey_pre_save, sender=Survey)
post_save.connect(survey_item_post_save, sender=SurveyItem)
post_delete.connect(survey_item_post_delete, sender=SurveyItem)
m2m_changed.connect(survey_item_m2m_changed, sender=SurveyItem.answers.through)
post_save.connect(attachment_post_save, sender=SurveyAttachment)
post_delete.connect(attachment_post_delete, sender=SurveyAttachment)
