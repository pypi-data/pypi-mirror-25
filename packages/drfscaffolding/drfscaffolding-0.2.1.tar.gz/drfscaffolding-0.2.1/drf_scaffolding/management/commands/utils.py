# -*- coding: utf-8 -*-
import os
import sys

from django.apps import apps
from django.conf import settings as dj_settings
from django.contrib.contenttypes.models import ContentType
from django.core.management.base import OutputWrapper
from django.core.management.color import color_style
from django.template import Context, Template

from . import settings


def write(msg, is_error=False):
    stdout = OutputWrapper(sys.stdout)
    style = color_style()
    if is_error:
        styling_msg = style.ERROR(msg)
    else:
        styling_msg = style.SUCCESS(msg)

    stdout.write(styling_msg)


def join_label_app(label, app, is_py_file=True):
    extension = '.py' if is_py_file else ''
    return '{0}/{1}{2}'.format(label, app, extension)


def file_exists(path):
    return os.path.isfile(path)


def create_file(path, context=None, template=None):
    if not file_exists(path):
        with open(path, 'w') as f:
            msg = join_label_app(
                'Writing: ', path, is_py_file=False)
            write(msg)
            if not context:
                context = Context()

            if not template:
                template = ''

            template_loaded = Template(template)
            api_text = template_loaded.render(context)
            f.write(api_text)


def create_init_file(path):
    url = join_label_app(path, '__init__')
    create_file(url)


def get_or_create_file(path, context=None, template=None):
    if not file_exists(path):
        create_file(path, context, template)


def dir_exists(path):
    return os.path.isdir(path)


def create_dir(path):
    return os.makedirs(path)


def get_or_create_dir(path):
    if not dir_exists(path):
        return create_dir(path)
    else:
        return True


def get_app_labels(app_labels):
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


def validate_paths(apps_path, file_type='api'):
    path_name = '%s_path' % file_type
    for app in apps_path:
        serializer_path = '{0}'.format(app[path_name])
        for model in app['models']:
            if model[file_type] is True:
                serializer_file = join_label_app(
                    serializer_path,
                    model['name'].lower()
                )

                if os.path.isfile(serializer_file):
                    msg = '{0} is already exists in app: {1}'.format(
                        file_type,
                        app['label']
                    )
                    write(msg, True)


def get_meta_model_config(model, file_type='api'):
    if hasattr(model._meta, 'drf_config'):
        drf_config = model._meta.drf_config
        model_config = {}
        model_config[file_type] = False

        if file_type not in drf_config:
            return model_config

        if 'scaffolding' not in drf_config[file_type]:
            return model_config

        if drf_config[file_type]['scaffolding'] is True:
            original_confs = drf_config[file_type]
            model_config = {
                'name': model.__name__
            }
            model_config[file_type] = True

            if 'methods' in original_confs:
                model_config['methods'] = original_confs['methods']
            else:
                model_config['methods'] = [
                    'CREATE',
                    'RETRIEVE',
                    'LIST',
                    'DELETE',
                    'UPDATE'
                ]

            if 'fields' in original_confs:
                model_config['fields'] = original_confs['fields']
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
            model_config[file_type] = False

        return model_config

    return None


def get_label_app_config(app_labels, api_version, file_type='api'):
    given_apps_path = []
    bad_app_labels = set()
    for app_label in app_labels:
        try:
            app = apps.get_app_config(app_label)
            models = []
            for m in apps.get_app_config(app_label).get_models():
                valid_model = get_meta_model_config(m, file_type)
                if valid_model:
                    models.append(valid_model)

            given_apps_path.append({
                'path': app.path,
                'label': app_label,
                'api_path': "{0}/viewsets".format(app.path),
                'serializer_path': "{0}/serializers".format(app.path),
                'form_path': "{0}/forms".format(app.path),
                'admin_path': "{0}/admin".format(app.path),
                'models': models,
                'api_version': api_version,
                'extra_options': {}
            })
        except LookupError:
            bad_app_labels.add(app_label)

    if bad_app_labels:
        for app_label in bad_app_labels:
            msg = "App '%s' could not be found." % app_label
            write(msg, True)
        sys.exit(2)

    if not given_apps_path:
        write("Apps could not be found.", True)
        sys.exit(2)

    return given_apps_path
