# -*- coding: utf-8 -*-
from django.conf import settings as dj_settings
from django.core.management import BaseCommand
from django.template import Context

from . import settings, templates
from .utils import (
    create_init_file,
    get_app_labels,
    get_label_app_config,
    get_or_create_dir,
    get_or_create_file,
    join_label_app,
    validate_paths
)


class Command(BaseCommand):
    help = "Create serializers from app models."

    can_import_settings = True
    requires_system_checks = False

    def add_arguments(self, parser):
        parser.add_argument(
            'args', metavar='app_label', nargs='*',
            help='Name of the application where you want to create the api.',
        )

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

    def handle(self, *app_labels, **options):
        PROJECT_NAME = dj_settings.BASE_DIR.split('/')[-1]
        API_VERSION = settings.DRF_SETTINGS['version']
        app_labels = get_app_labels(app_labels)

        #
        # Make sure the app they asked for exists
        #
        given_apps_path = get_label_app_config(
            app_labels,
            API_VERSION,
            'serializer'
        )

        #
        # Validate applications api path or serializer path exists
        #
        validate_paths(given_apps_path, file_type='serializer')

        for app in given_apps_path:
            get_or_create_dir(app['serializer_path'])
            for model in app['models']:
                if model['serializer'] is True:
                    self.write_serializer(app, model, PROJECT_NAME)
