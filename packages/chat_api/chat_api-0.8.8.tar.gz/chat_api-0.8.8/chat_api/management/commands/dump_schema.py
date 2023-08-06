# -*- coding: utf-8 -*-
from chat_api.models import Answer, AttachmentTemplate, Group, Question, Schema
from django.core import serializers
from django.core.management.base import BaseCommand, CommandError
from django.db import DEFAULT_DB_ALIAS


class Command(BaseCommand):
    help = "Dumps a single schema (with questions, answers & attachment templates) into a fixture"

    def add_arguments(self, parser):
        parser.add_argument(
            "--format", default="json", dest="format", help="Specifies the output serialization format for fixtures.",
        )
        parser.add_argument(
            "--indent", default=4, dest="indent", type=int,
            help="Specifies the indent level to use when pretty-printing output.",
        )
        parser.add_argument(
            "--database", action="store", dest="database", default=DEFAULT_DB_ALIAS,
            help="Nominates a specific database to dump fixtures from. Defaults to the 'default' database.",
        )
        parser.add_argument(
            "--name", action="store", dest="name", default=None,
            help="Name of the schema. The latest schema with given name will be dumped. "
                 "Either Name or PK must be supplied.",
        )
        parser.add_argument(
            "--pk", type=int, dest="pk", default=None,
            help="PK of the schema. Either Name or PK must be supplied.",
        )
        parser.add_argument(
            "-o", "--output", default=None, dest="output",
            help="Specifies file to which the output is written."
        )

    @classmethod
    def get_objects_count(cls, schema, using):
        yield 1  # schema
        yield Group.objects.using(using).filter(schema=schema).count()

        question_ids = list(Question.objects.using(using).filter(schema=schema).values_list("id", flat=True))
        yield len(question_ids)
        yield Answer.objects.using(using).filter(question_id__in=question_ids).count()
        yield AttachmentTemplate.objects.using(using).filter(question_id__in=question_ids).count()

    @classmethod
    def get_objects(cls, schema, using):
        yield schema
        for group in Group.objects.using(using).filter(schema=schema):
            yield group

        question_ids = []
        for question in Question.objects.using(using).filter(schema=schema):
            yield question
            question_ids.append(question.pk)

        for answer in Answer.objects.using(using).filter(question_id__in=question_ids):
            yield answer

        for attachment_template in AttachmentTemplate.objects.using(using).filter(question_id__in=question_ids):
            yield attachment_template

    @classmethod
    def dump_schema(cls, schema, stream, fmt="json", using=DEFAULT_DB_ALIAS, indent=4, progress_output=False,
                    object_count=0):
        serializers.serialize(
            fmt, cls.get_objects(schema, using), indent=indent, use_natural_foreign_keys=False,
            use_natural_primary_keys=False, stream=stream, progress_output=progress_output,
            object_count=object_count,
        )

    def handle(self, *app_labels, **options):
        # get & check parameters
        fmt = options["format"]
        indent = options["indent"]
        using = options["database"]
        show_traceback = options['traceback']
        name = options["name"]
        pk = options["pk"]
        output = options["output"]

        if fmt not in serializers.get_public_serializer_formats():
            try:
                serializers.get_serializer(fmt)
            except serializers.SerializerDoesNotExist:
                pass

            raise CommandError("Unknown serialization format: %s" % fmt)

        if not pk and not name:
            raise CommandError("Either Name or PK must be specified.")
        if pk and name:
            raise CommandError("Only one of either Name or PK can be specified.")

        if pk:
            schema = Schema.objects.using(using).filter(pk=pk).first()
        else:
            schema = Schema.objects.using(using).filter(name=name).order_by("-id").first()

        if not schema:
            raise CommandError("Schema not found.")

        # run the dumping
        try:
            self.stdout.ending = None
            progress_output = None
            object_count = 0
            # If dumpdata is outputting to stdout, there is no way to display progress
            if (output and self.stdout.isatty() and options['verbosity'] > 0):
                progress_output = self.stdout
                object_count = sum(self.get_objects_count(schema, using))
            stream = open(output, 'w') if output else None
            try:
                self.dump_schema(schema, stream or self.stdout, fmt, using, indent, progress_output, object_count)
            finally:
                if stream:
                    stream.close()
        except Exception as e:
            if show_traceback:
                raise
            raise CommandError("Unable to serialize database: %s" % e)
