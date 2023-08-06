from chat_api.models import Schema
from chat_api.schemas.signals import schema_uploaded_signal
from django.core import serializers
from django.core.management.base import BaseCommand, CommandError
from django.core.management.color import no_style
from django.db import connections, DatabaseError, DEFAULT_DB_ALIAS, IntegrityError, router, transaction
from django.utils.encoding import force_text

import sys
import warnings


class FixtureLoader(object):
    def __init__(self, fixture=None, fixture_file_name=None, ignore=True, using=DEFAULT_DB_ALIAS, verbosity=0,
                 output=sys.stdout):
        # params
        self.ignore = ignore
        self.verbosity = verbosity
        self.using = using
        self.fixture_file_name = fixture_file_name
        self.output = output

        # Keep a count of the installed objects and fixtures
        self.fixture_count = 0
        self.loaded_object_count = 0
        self.fixture = fixture
        self.models = set()

    def run(self):
        if self.fixture_file_name:
            try:
                fixture = open(self.fixture_file_name, "rt")
            except Exception as e:
                warnings.warn("Could not open file: %s", self.fixture_file_name)
                return
        else:
            fixture = self.fixture

        connection = connections[self.using]

        with connection.constraint_checks_disabled():
            self.load_fixture(fixture)

        table_names = [model._meta.db_table for model in self.models]
        try:
            connection.check_constraints(table_names=table_names)
        except Exception as e:
            e.args = ("Problem installing fixtures: %s" % e,)
            raise

        # If we found even one object in a fixture, we need to reset the
        # database sequences.
        if self.loaded_object_count > 0:
            sequence_sql = connection.ops.sequence_reset_sql(no_style(), self.models)
            if sequence_sql:
                if self.verbosity >= 2:
                    self.output.write("Resetting sequences\n")
                with connection.cursor() as cursor:
                    for line in sequence_sql:
                        cursor.execute(line)

        if self.verbosity >= 1:
            self.output.write(
                "Installed %d object(s) from %d fixture(s)"
                % (self.loaded_object_count, self.fixture_count)
            )
        # send signal
        uploaded_schema = Schema.objects.order_by("-id").first()
        schema_uploaded_signal.send(sender=Schema, instance=uploaded_schema)

    def load_fixture(self, fixture):
        show_progress = self.verbosity >= 3
        obj_map = {}

        try:
            self.fixture_count += 1
            if self.verbosity >= 2:
                self.output.write("Installing fixture \"%s\"" % (self.fixture_file_name))

            objects = serializers.deserialize(
                "json", fixture, using=self.using, ignorenonexistent=self.ignore,
            )

            for obj in objects:
                self.loaded_object_count += 1
                if router.allow_migrate_model(self.using, obj.object.__class__):
                    self.models.add(obj.object.__class__)

                # change an id of the object to a new one
                old_obj_id = obj.object.pk
                obj.object.pk = None  # create a new object instead of updating old one

                # update all ids to the ones that are mapped
                for field in obj.object._meta.fields:
                    if field.get_internal_type() == "ForeignKey" and field.related_model in obj_map:
                        pk = getattr(obj.object, field.name + "_id")
                        if pk in obj_map[field.related_model]:
                            setattr(obj.object, field.name + "_id", obj_map[field.related_model][pk])

                try:
                    obj.save(using=self.using)
                    if obj.object.__class__ not in obj_map:
                        obj_map[obj.object.__class__] = {}
                    obj_map[obj.object.__class__][old_obj_id] = obj.object.pk

                    if show_progress:
                        self.output.write(
                            '\rProcessed %i object(s).' % self.loaded_object_count,
                            ending=''
                        )
                except (DatabaseError, IntegrityError) as e:
                    e.args = ("Could not load %(app_label)s.%(object_name)s(pk=%(pk)s): %(error_msg)s" % {
                        'app_label': obj.object._meta.app_label,
                        'object_name': obj.object._meta.object_name,
                        'pk': obj.object.pk,
                        'error_msg': force_text(e)
                    },)
                    raise
        except Exception as e:
            if not isinstance(e, CommandError):
                e.args = ("Problem installing fixture '%s': %s" % (self.fixture_file_name, e),)
            raise
        finally:
            fixture.close()
            # Warn if the fixture we loaded contains 0 objects.
            if self.loaded_object_count == 0:
                warnings.warn(
                    "No fixture data found for '%s'. (File format may be invalid.)" % self.fixture_file_name,
                    RuntimeWarning
                )


class Command(BaseCommand):
    help = "Load the schema from fixture, ignoring original objects ids."

    def add_arguments(self, parser):
        parser.add_argument("args", nargs="+", help="Fixture file name.")
        parser.add_argument(
            "--database", action="store", dest="database", default=DEFAULT_DB_ALIAS,
            help="Nominates a specific database to load fixtures into. Defaults to the \"default\" database.",
        )
        parser.add_argument(
            "--ignorenonexistent", "-i", action="store_true", dest="ignore", default=False,
            help="Ignores entries in the serialized data for fields that do not currently exist on the model.",
        )

    def handle(self, fixture_file_name, **options):
        ignore = options['ignore']
        using = options['database']
        verbosity = options['verbosity']

        with transaction.atomic(using=using):
            FixtureLoader(
                fixture_file_name=fixture_file_name, ignore=ignore, using=using, verbosity=verbosity, output=self.stdout
            ).run()

        # Close the DB connection -- unless we're still in a transaction. This
        # is required as a workaround for an  edge case in MySQL: if the same
        # connection is used to create tables, load data, and query, the query
        # can return incorrect results. See Django #7572, MySQL #37735.
        if transaction.get_autocommit(using):
            connections[using].close()
