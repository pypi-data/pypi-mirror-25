# -*- coding: UTF-8 -*-
from __future__ import absolute_import, unicode_literals, print_function

from django.apps import apps
from dinjatags import Library
from importlib import import_module
from pkgutil import iter_modules


def load_jinja2tags(env, tag_module='jinja2tags'):
    for app_config in apps.get_app_configs():
        try:
            module = import_module(".%s" % tag_module, app_config.name)
        except ImportError:
            continue

        iter_submodules(env, module)


def iter_submodules(env, module):
    for importer, modname, ispkg in iter_modules(module.__path__):
        submodule = importer.find_module(modname).load_module(modname)
        iter_submodule_contents(env, submodule)


def iter_submodule_contents(env, submodule):
    for name in dir(submodule):
        library_candidate = getattr(submodule, name)
        if issubclass(type(library_candidate), Library):
            if len(library_candidate.tags) > 0:
                env.globals.update(
                    library_candidate.tags
                )
            if len(library_candidate.filters) > 0:
                env.filters.update(
                    library_candidate.filters
                )