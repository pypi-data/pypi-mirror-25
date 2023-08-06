# -*- coding: utf-8 -*-
import os
import sys

from django.apps import apps
from django.conf import settings as dj_settings
from django.contrib.contenttypes.models import ContentType
from django.core.management import BaseCommand
from django.template import Context

from . import settings, templates
from .utils import (
    create_init_file,
    get_or_create_dir,
    get_or_create_file,
    join_label_app,
    write
)


class Command(BaseCommand):
    help = "Starts an api from app models for development."

    can_import_settings = True
    requires_system_checks = False

    def add_arguments(self, parser):
        parser.add_argument(
            'args', metavar='app_label', nargs='*',
            help='Name of the application where you want create the api.',
        )

    def get_app_labels(self, app_labels):
        exclude_apps = settings.DRF_SETTINGS['exclude_apps']

        if len(app_labels) == 0:
            if hasattr(dj_settings, 'LOCAL_APPS'):
                apps = [i.split('.')[-1] for i in dj_settings.LOCAL_APPS]
            else:
                apps = ContentType.objects.exclude(
                    app_label__in=exclude_apps
                ).values_list(
                    'app_label',
                    flat=True
                ).distinct()

            return set(apps)

        return set(app_labels)

    def write_serializer(self, config_app, model, project_name):
        #
        # create init file into serializers folder
        #
        create_init_file(config_app['serializer_path'])

        #
        # Create serializer file
        #
        serializer_path = join_label_app(
            config_app['serializer_path'],
            model['name'].lower()
        )

        context = Context({
            'project_name': project_name,
            'app_name': config_app['label'],
            'model': model
        })

        get_or_create_file(
            serializer_path,
            context,
            templates.SERIALIZER_TEMPLATE
        )

    def get_meta_model_config(self, model):
        if hasattr(model._meta, 'drf_config'):
            drf_config = model._meta.drf_config
            model_config = {
                'serializer': False
            }

            if 'serializer' not in drf_config:
                return model_config

            if 'scaffolding' not in drf_config['serializer']:
                return model_config

            if drf_config['serializer']['scaffolding'] is True:
                serializer = drf_config['serializer']
                model_config = {
                    'name': model.__name__,
                    'serializer': True
                }

                if 'fields' in serializer:
                    model_config['fields'] = serializer['fields']
                else:
                    fields = []
                    for f in model._meta.get_fields():
                        try:
                            if not f.null:
                                fields.append(f.name)
                        except AttributeError:
                            pass

                    model_config['fields'] = fields

            else:
                model_config['serializer'] = False

            return model_config

        return None

    def get_label_app_config(self, app_labels, api_version):
        given_apps_path = []
        bad_app_labels = set()
        for app_label in app_labels:
            try:
                app = apps.get_app_config(app_label)
                models = []
                for m in apps.get_app_config(app_label).get_models():
                    valid_model = self.get_meta_model_config(m)
                    if valid_model:
                        models.append(valid_model)

                given_apps_path.append({
                    'path': app.path,
                    'label': app_label,
                    'api_path': "{0}/viewsets".format(app.path),
                    'serializer_path': "{0}/serializers".format(app.path),
                    'models': models,
                    'api_version': api_version,
                    'extra_options': {}
                })
            except LookupError:
                bad_app_labels.add(app_label)

        if bad_app_labels:
            for app_label in bad_app_labels:
                msg = "App '%s' could not be found." % app_label
                write(msg)
            sys.exit(2)

        if not given_apps_path:
            write("Apps could not be found.")
            sys.exit(2)

        return given_apps_path

    def validate_paths(self, apps_path):
        for app in apps_path:
            serializer_path = '{0}'.format(app['serializer_path'])
            for model in app['models']:
                if model['serializer'] is True:
                    serializer_file = join_label_app(
                        serializer_path,
                        model['name'].lower()
                    )

                    if os.path.isfile(serializer_file):
                        msg = 'api is already exist in app: %s' % app['label']
                        write(msg)

    def handle(self, *app_labels, **options):
        PROJECT_NAME = dj_settings.BASE_DIR.split('/')[-1]
        API_VERSION = settings.DRF_SETTINGS['version']
        app_labels = self.get_app_labels(app_labels)

        #
        # Make sure the app they asked for exists
        #
        given_apps_path = self.get_label_app_config(app_labels, API_VERSION)

        #
        # Validate applications api path or serializer path exists
        #
        self.validate_paths(given_apps_path)

        for app in given_apps_path:
            get_or_create_dir(app['serializer_path'])
            for model in app['models']:
                if model['serializer'] is True:
                    self.write_serializer(app, model, PROJECT_NAME)
