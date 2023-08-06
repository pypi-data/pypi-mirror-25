# -*- coding: utf-8 -*-
from chat_api.common import AttachmentTypes
from chat_api.schemas.utils import validate_variable_modifications
from chat_api.settings import chat_settings
from chat_api.utils.fields import JSONField
from collections import defaultdict
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import ugettext_lazy as _
from simpleeval import simple_eval


class Question(models.Model):
    TYPE_CHOICE = "choice"
    TYPE_MULTICHOICE = "multichoice"
    TYPE_TEXT = "text"
    TYPE_DATE = "date"
    TYPE_TIME = "time"
    TYPE_DATETIME = "datetime"
    TYPE_INT = "int"
    TYPE_FLOAT = "float"
    TYPE_RANGE = "range"
    TYPE_MESSAGE = "message"
    TYPE_FORK = "fork"
    TYPE_CONTROL = "control"
    TYPE_CHOICES = (
        (TYPE_CHOICE, "Choice"),
        (TYPE_MULTICHOICE, "Multichoice"),
        (TYPE_TEXT, "Text"),
        (TYPE_DATE, "Date"),
        (TYPE_TIME, "Time"),
        (TYPE_DATETIME, "Datetime"),
        (TYPE_INT, "Int"),
        (TYPE_FLOAT, "Float"),
        (TYPE_RANGE, "Range"),
        (TYPE_MESSAGE, "Message (no answers)"),
        (TYPE_CONTROL, "Control (no answer)"),
        (TYPE_FORK, "Fork (not displayed)"),
    )

    CHOICES_TYPES = (TYPE_CHOICE, TYPE_MULTICHOICE)

    choice_open = models.BooleanField(default=False)
    group = models.ForeignKey("chat_api.Group", null=True, blank=True, on_delete=models.CASCADE,
                              related_name="questions")
    has_attachments = models.BooleanField(default=False)
    meta = JSONField(null=True, blank=True)
    next_qid = models.IntegerField(null=True, blank=True, help_text=_("For last question set -1."))
    position = models.IntegerField(db_index=True)
    qid = models.IntegerField(db_index=True)
    range_from = models.FloatField(null=True, blank=True)
    range_to = models.FloatField(null=True, blank=True)
    required = models.BooleanField(default=False)
    schema = models.ForeignKey("chat_api.Schema", on_delete=models.CASCADE, related_name="questions")
    text = models.TextField()
    type = models.CharField(max_length=50, choices=TYPE_CHOICES)
    comments = models.TextField(null=True, blank=True)
    # variable_modifications = [["x", "x + 1"], [y, x], [x, x * y + x**2]]
    # unknown variables are equal to 0
    # everything is a float
    variable_modifications = JSONField(blank=True, default=list)
    # forking_rules = [["z", "x <= y"], ["1", "x > y"]]
    forking_rules = JSONField(blank=True, default=list)
    show_as_type = models.CharField(max_length=255, default="automated_message")

    def answers_next_qid_list(self):
        if self.type in (self.TYPE_CHOICE, self.TYPE_MULTICHOICE):
            return ", ".join(map(str, self.answers.all().values_list("next_qid", flat=True)))
        return ""

    def get_fork_for_variables(self, variables_pool):
        if variables_pool:
            variables_pool = defaultdict(float, variables_pool)
        else:
            # Workaround for strange behaviour of simpleeval - it accepts defaultdict w/o problems,
            # as long as there is at least one element inside. Otherwise it throws an error.
            variables_pool = defaultdict(float, {"_______________": 0})

        for qid, condition in self.forking_rules:
            if simple_eval(condition, names=variables_pool):
                return int(simple_eval(qid, names=variables_pool))
        return -1

    def __str__(self):
        return "%d: %s" % (self.id, self.text)

    def clean(self):
        errors = {}
        possible_error_fields = ["next_qid", "choice_open", "forking_rules", "range_from",
                                 "range_to"]
        for field in possible_error_fields:
            errors[field] = []

        if self.type == self.TYPE_RANGE:
            if not self.range_from:
                errors["range_from"].append(_("This field is required."))
            if not self.range_to:
                errors["range_to"].append(_("This field is required."))

        if self.type not in self.CHOICES_TYPES:
            if self.choice_open:
                errors["choice_open"].append(_("Allowed only for types: choice and multichoice."))
            if not self.next_qid and self.type != self.TYPE_FORK:
                errors["next_qid"].append(_("This field is required."))

        if self.type != self.TYPE_FORK and self.forking_rules != []:
            errors["forking_rules"].append(_("Allowed only for type: fork."))

        if self.type == self.TYPE_FORK:
            if not self.forking_rules:
                errors["forking_rules"].append(_("This field is required."))

            for rule in self.forking_rules:
                if not type(rule) == list:
                    errors["forking_rules"].append(
                        _("%s is not a list" % rule))
                elif len(rule) != 2:
                    errors["forking_rules"].append(
                        _("[%s] is not two elements list." % ", ".join(str(r) for r in rule)))
                else:
                    try:
                        compile(rule[0], "fakemodule", "eval")
                    except SyntaxError:
                        errors["forking_rules"].append(
                            _("%s is not valid python variable name." % rule[0]))
                    if len(''.join(rule[1].split())) <= 5 and " " not in rule[1]:
                        # abc is not an expression.
                        # a * c is
                        errors["forking_rules"].append(
                            _("[%s] is not an expression." % rule[1]))

                    if " " not in rule[1]:
                        # abcdef is not an expression.
                        errors["forking_rules"].append(
                            _("[%s] is not an expression." % rule[1]))
                    # compile dies if first parameter is not python expression
                    try:
                        compile(rule[1], "fakemodule", "eval")
                    except SyntaxError:
                        errors["forking_rules"].append(
                            _("[%s] is not valid python expression."
                              " Please separate variables and operators with spaces." % rule[1]))

        errors = validate_variable_modifications(self, errors)

        real_errors = {}
        for e in errors:
            if len(errors[e]):
                real_errors[e] = errors[e]

        if real_errors:
            raise ValidationError(real_errors)

    class Meta:
        unique_together = (("qid", "schema"), ("position", "schema"))
        ordering = ("position",)
        app_label = "chat_api"


class Group(models.Model):
    name = models.CharField(max_length=100, db_index=True)
    position = models.IntegerField(db_index=True)
    schema = models.ForeignKey("chat_api.Schema", on_delete=models.CASCADE, related_name="groups")

    def __str__(self):
        return self.name

    class Meta:
        unique_together = (("name", "schema"), ("position", "schema"))
        ordering = ("position",)
        app_label = "chat_api"


class Schema(models.Model):
    deprecated = models.BooleanField(default=False, db_index=True)
    name = models.CharField(max_length=100)
    published = models.BooleanField(default=False, db_index=True)
    type = models.CharField(max_length=100, choices=chat_settings.TYPES_SCHEMA, db_index=True)
    version = models.IntegerField(default=1)

    def __str__(self):
        return "%s (%d)" % (self.name, self.version)

    def publish(self):
        Schema.objects.filter(name=self.name, published=True).update(deprecated=True)
        self.published = True
        self.save()

    def copy_as_unpublished(self):
        """Copy schema as unpublished, so it can be edited."""
        # copy the schema
        questions = list(self.questions.all())
        groups = list(self.groups.all())
        self.published = False
        self.deprecated = False
        self.version += 1
        self.pk = None  # will copy the object
        self.save()

        groups_map = {}
        for group in groups:
            groups_map[group.pk] = group
            group.pk = None
            group.schema_id = self.pk
            group.save()

        # copy questions
        for question in questions:
            answers = list(question.answers.all())
            attachments = list(question.attachments.all())

            question.pk = None
            question.schema_id = self.pk
            if question.group_id:
                question.group_id = groups_map[question.group_id].pk
            question.save()

            # copy answers
            for answer in answers:
                answer.pk = None
                answer.question_id = question.pk
                answer.save()

            # copy content objects
            for attachment in attachments:
                attachment.pk = None
                attachment.question_pk = question.pk
                attachment.save()

    @property
    def not_grouped_questions(self):
        return Question.objects.filter(schema_id=self.id, group__isnull=True)

    class Meta:
        unique_together = (("name", "version"), )
        app_label = "chat_api"


class Answer(models.Model):
    meta = JSONField(null=True, blank=True)
    next_qid = models.IntegerField()
    position = models.IntegerField(db_index=True)
    question = models.ForeignKey("chat_api.Question", on_delete=models.CASCADE, related_name="answers")
    text = models.TextField()
    comments = models.TextField(null=True, blank=True)
    variable_modifications = JSONField(blank=True, default=list)
    exclusive = models.BooleanField(default=False)

    class Meta:
        unique_together = (("position", "question"), )
        ordering = ("position",)
        app_label = "chat_api"

    def clean(self):
        errors = {}
        errors["next_qid"] = []

        if not Question.objects.filter(qid=self.next_qid).exists():
            errors["next_qid"].append(_("Next question id(next_qid) points to not existing question."))

        errors = validate_variable_modifications(self, errors)

        real_errors = {}
        for e in errors:
            if len(errors[e]):
                real_errors[e] = errors[e]

        if real_errors:
            raise ValidationError(real_errors)


class AttachmentTemplate(models.Model):
    description = models.TextField(blank=True)
    object_id = models.PositiveIntegerField(null=True, blank=True)
    content_type = models.ForeignKey("contenttypes.ContentType", null=True, db_index=False, on_delete=models.CASCADE)
    options = JSONField(null=True, blank=True)
    question = models.ForeignKey("chat_api.Question", null=True, blank=True, on_delete=models.CASCADE,
                                 related_name="attachments")
    file = models.FileField(null=True, blank=True)
    url = models.URLField(null=True, blank=True)
    thumbnail = JSONField(null=True, blank=True)
    thumbnail_image = models.ImageField(null=True, blank=True)
    title = models.CharField(max_length=255, blank=True)
    type = models.CharField(max_length=50, choices=AttachmentTypes.TYPE_CHOICES)

    class Meta:
        app_label = "chat_api"
