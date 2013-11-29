#-*- coding: utf-8 -*-
import inspect
import sys

from django.core import exceptions
from django.utils.importlib import import_module


CLASS_PATH_ERROR = 'django-fairepart is unable to interpret settings value for %s. '\
                   '%s should be in the form of a tupple: '\
                   '(\'path.to.models.Class\', \'app_label\').'


def load_class(class_path, setting_name=None):
    """
    Loads a class given a class_path. The setting value may be a string or a
    tuple.

    The setting_name parameter is only there for pretty error output, and
    therefore is optional
    """
    if not isinstance(class_path, basestring):
        try:
            class_path, app_label = class_path
        except:
            if setting_name:
                raise exceptions.ImproperlyConfigured(CLASS_PATH_ERROR % (
                    setting_name, setting_name))
            else:
                raise exceptions.ImproperlyConfigured(CLASS_PATH_ERROR % (
                    'this setting', 'It'))

    try:
        class_module, class_name = class_path.rsplit('.', 1)
    except ValueError:
        if setting_name:
            txt = '%s isn\'t a valid module. Check your %s setting' % (
                class_path, setting_name)
        else:
            txt = '%s isn\'t a valid module.' % class_path
        raise exceptions.ImproperlyConfigured(txt)

    try:
        mod = import_module(class_module)
    except ImportError, e:
        if setting_name:
            txt = 'Error importing backend %s: "%s". Check your %s setting' % (
                class_module, e, setting_name)
        else:
            txt = 'Error importing backend %s: "%s".' % (class_module, e)

        raise exceptions.ImproperlyConfigured(txt)

    try:
        clazz = getattr(mod, class_name)
    except AttributeError:
        if setting_name:
            txt = ('Backend module "%s" does not define a "%s" class. Check'
                   ' your %s setting' % (class_module, class_name,
                                         setting_name))
        else:
            txt = 'Backend module "%s" does not define a "%s" class.' % (
                class_module, class_name)
        raise exceptions.ImproperlyConfigured(txt)
    return clazz


def reraise_as(new_exception_or_type):
    """
    Obtained from https://github.com/dcramer/reraise/blob/master/src/reraise.py
    >>> try:
    >>>     do_something_crazy()
    >>> except Exception:
    >>>     reraise_as(UnhandledException)
    """
    __traceback_hide__ = True  # NOQA

    e_type, e_value, e_traceback = sys.exc_info()

    if inspect.isclass(new_exception_or_type):
        new_type = new_exception_or_type
        new_exception = new_exception_or_type()
    else:
        new_type = type(new_exception_or_type)
        new_exception = new_exception_or_type

    new_exception.__cause__ = e_value

    try:
        raise new_type, new_exception, e_traceback
    finally:
        del e_traceback
