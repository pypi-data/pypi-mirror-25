# -*- coding: utf-8 -*-

from django.core.management import BaseCommand, call_command

from .utils import write


class Command(BaseCommand):
    help = "Starts an full API and admin from app models."

    can_import_settings = True
    requires_system_checks = False

    def add_arguments(self, parser):
        parser.add_argument(
            'args', metavar='app_label', nargs='*',
            help='Name of the application where you want to do scaffolding.',
        )

    def handle(self, *app_labels, **options):
        if app_labels:
            for label in app_labels:
                call_command('createserializers', label)
                call_command('createforms', label)
                call_command('createadmin', label)
                call_command('createapi', label)
        else:
            call_command('createserializers')
            call_command('createforms')
            call_command('createadmin')
            call_command('createapi')

        write('hocus pocus!!!')
