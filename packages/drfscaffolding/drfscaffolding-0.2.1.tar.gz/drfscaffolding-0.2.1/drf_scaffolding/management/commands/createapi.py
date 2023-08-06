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
    help = "Starts an api from app models for development."

    can_import_settings = True
    requires_system_checks = False

    def add_arguments(self, parser):
        parser.add_argument(
            'args', metavar='app_label', nargs='*',
            help='Name of the application where you want create the api.',
        )

    def write_api(self, config_app, model, project_name):
        #
        # create init file into viewsets folder
        #
        create_init_file(config_app['api_path'])

        #
        # Create api file
        #
        viewset_path = join_label_app(
            config_app['api_path'],
            model['name'].lower()
        )

        context = Context({
            'project_name': project_name,
            'app_name': config_app['label'],
            'api_version': config_app['api_version'],
            'model': model
        })

        get_or_create_file(viewset_path, context, templates.API_TEMPLATE)

    def write_routes(self, config_app, models, project_name, api_version):
        route_path = join_label_app(
            config_app['path'],
            'api'
        )

        context = Context({
            'models': models,
            'project_name': project_name,
            'api_version': api_version
        })
        #
        # create routes file in app root, for example: polls/api.py
        #
        get_or_create_file(route_path, context, templates.ROUTE_TEMPLATE)

    def handle(self, *app_labels, **options):
        PROJECT_NAME = dj_settings.BASE_DIR.split('/')[-1]
        API_VERSION = settings.DRF_SETTINGS['version']
        app_labels = get_app_labels(app_labels)

        #
        # Make sure the app they asked for exists
        #
        given_apps_path = get_label_app_config(app_labels, API_VERSION)

        #
        # Validate applications api path or serializer path exists
        #
        validate_paths(given_apps_path)

        for app in given_apps_path:
            models = [m for m in app['models'] if m['api'] is True]
            has_models = len(models) > 0

            if has_models:
                get_or_create_dir(app['api_path'])

            for model in app['models']:
                if model['api'] is True:
                    self.write_api(app, model, PROJECT_NAME)

            if has_models:
                self.write_routes(
                    app,
                    models,
                    PROJECT_NAME, API_VERSION
                )
