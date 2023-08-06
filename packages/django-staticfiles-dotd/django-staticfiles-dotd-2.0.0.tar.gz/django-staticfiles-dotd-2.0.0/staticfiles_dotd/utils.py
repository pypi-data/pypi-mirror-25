import sys
import functools

from django.utils.module_loading import import_string

from . import app_settings


def render(filename):
    with open(filename, 'rb') as f:
        result = f.read()

    for x in app_settings.RENDER_PIPELINE:
        result = import_string(x)(filename, result)

    return result


def monkeypatch(new, modname, target):
    __import__(modname)
    module = sys.modules[modname]

    func = getattr(module, target)
    functools.update_wrapper(new, func)
    setattr(module, target, new)
