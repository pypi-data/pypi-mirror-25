# -*- coding: utf-8 -*-
from django.conf import settings as dj_settings
from django.core.management import BaseCommand
from django.template import Context

from . import settings, templates
from .utils import (
    get_app_labels,
    get_label_app_config,
    get_or_create_file,
    join_label_app,
    validate_paths
)


class Command(BaseCommand):
    help = "Starts admin file from app models."

    can_import_settings = True
    requires_system_checks = False

    def add_arguments(self, parser):
        parser.add_argument(
            'args', metavar='app_label', nargs='*',
            help='Name of the application where you want to create the admin.',
        )

    def write_admin(self, config_app, models, project_name):
        #
        # Create admin file
        #
        file_path = config_app['admin_path'][:-6]
        admin_path = join_label_app(file_path, 'admin')

        context = Context({
            'project_name': project_name,
            'app_name': config_app['label'],
            'models': models
        })

        get_or_create_file(
            admin_path,
            context,
            templates.ADMIN_TEMPLATE
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
            'admin'
        )

        #
        # Validate applications admin path exists
        #
        validate_paths(given_apps_path, file_type='admin')

        for app in given_apps_path:
            models = [m for m in app['models'] if m['admin'] is True]
            has_models = len(models) > 0

            if has_models:
                self.write_admin(app, models, PROJECT_NAME)
