# -*- coding: utf-8 -*-
import os
import sys

from django.template import Context, Template


def write(msg):
    sys.stdout.write(msg)


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
