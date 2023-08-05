# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from flask.globals import LocalProxy, partial
from flask.globals import _lookup_app_object as _lookup_app_context_object


def _lookup_app_object(name):
    app = LocalProxy(partial(_lookup_app_context_object, 'app'))
    return getattr(app, name)


settings = LocalProxy(partial(_lookup_app_object, 'settings'))
