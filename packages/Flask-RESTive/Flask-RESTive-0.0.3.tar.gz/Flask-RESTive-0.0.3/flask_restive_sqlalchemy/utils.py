# -*- coding: utf-8 -*-
"""
The configuration code is copied from Flask-SQLAlchemy.
https://github.com/mitsuhiko/flask-sqlalchemy

Copyright (c) 2014 by Armin Ronacher.
"""
from __future__ import unicode_literals

import os

from sqlalchemy.engine.url import make_url


def make_connection_settings(app):
    uri = app.config.get('SQLALCHEMY_DATABASE_URI', 'sqlite:///:memory:')
    info = make_url(uri)
    options = {'convert_unicode': True}
    _apply_pool_defaults(app, options)
    _apply_driver_hacks(app, info, options)
    return info, options


def _apply_pool_defaults(app, options):

    def _setdefault(optionkey, configkey):
        value = app.config.get(configkey)
        if value is not None:
            options[optionkey] = value

    _setdefault('echo', 'SQLALCHEMY_ECHO')
    _setdefault('pool_size', 'SQLALCHEMY_POOL_SIZE')
    _setdefault('pool_timeout', 'SQLALCHEMY_POOL_TIMEOUT')
    _setdefault('pool_recycle', 'SQLALCHEMY_POOL_RECYCLE')
    _setdefault('poolclass', 'SQLALCHEMY_POOL_CLASS')
    _setdefault('max_overflow', 'SQLALCHEMY_MAX_OVERFLOW')


def _apply_driver_hacks(app, info, options):
    """This method is called before engine creation and used to inject
    driver specific hacks into the options.  The `options` parameter is
    a dictionary of keyword arguments that will then be used to call
    the :func:`sqlalchemy.create_engine` function.

    The default implementation provides some saner defaults for things
    like pool sizes for MySQL and sqlite.  Also it injects the setting of
    `SQLALCHEMY_NATIVE_UNICODE`.
    """
    if info.drivername.startswith('mysql'):
        info.query.setdefault('charset', 'utf8')
        if info.drivername != 'mysql+gaerdbms':
            options.setdefault('pool_size', 10)
            options.setdefault('pool_recycle', 7200)

    elif info.drivername == 'sqlite':
        pool_size = options.get('pool_size')
        detected_in_memory = False
        if info.database in (None, '', ':memory:'):
            detected_in_memory = True
            from sqlalchemy.pool import StaticPool
            options['poolclass'] = StaticPool
            if 'connect_args' not in options:
                options['connect_args'] = {}
            options['connect_args']['check_same_thread'] = False

            # we go to memory and the pool size was explicitly set
            # to 0 which is fail.  Let the user know that
            if pool_size == 0:
                raise RuntimeError('SQLite in memory database with an '
                                   'empty queue not possible due to data '
                                   'loss.')
        # if pool size is None or explicitly set to 0 we assume the
        # user did not want a queue for this sqlite connection and
        # hook in the null pool.
        elif not pool_size:
            from sqlalchemy.pool import NullPool
            options['poolclass'] = NullPool

        # if it's not an in memory database we make the path absolute.
        if not detected_in_memory:
            info.database = os.path.join(app.root_path, info.database)
