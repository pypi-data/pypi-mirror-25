# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from flask_restful import Api as BaseApi
from marshmallow.validate import ValidationError

from flask_restive.exceptions import ResourceError


class Api(BaseApi):
    """
    The main entry point for the application.
    You need to initialize it with a Flask Application: ::

    >>> app = Flask(__name__)
    >>> api = flask_restive.Api(app)

    Alternatively, you can use :meth:`init_app` to set the Flask application
    after it has been constructed.

    :param app: the Flask application or blueprint object
    :type app: flask.Flask
    :type app: flask.Blueprint
    :param prefix: Prefix all routes with a value, eg "/api/v1"
    :type prefix: str
    :param api_resources: List of tuples (resource, route).
        Multiple routes allowed also (resource, (route1, route2)).
    :type resources: list
    :param default_mediatype: The default media type to return
    :type default_mediatype: str
    :param decorators: Decorators to attach to every resource
    :type decorators: list
    :param catch_all_404s: Use :meth:`handle_error`
        to handle 404 errors throughout your app
    :param serve_challenge_on_401: Whether to serve a challenge response to
        clients on receiving 401. This usually leads to a username/password
        popup in web browers.
    :param url_part_order: A string that controls the order that the pieces
        of the url are concatenated when the full url is constructed.  'b'
        is the blueprint (or blueprint registration) prefix, 'a' is the api
        prefix, and 'e' is the path component the endpoint is added with
    :type catch_all_404s: bool
    :param errors: A dictionary to define a custom response for each
        exception or error raised during a request
    :type errors: dict
    """

    def __init__(self, app=None, prefix='',
                 api_resources=None, *args, **kwargs):
        self.prefix = prefix
        self.endpoint_prefix = self.prefix.replace('/', '_').strip('_')
        self.api_resources = api_resources or []
        super(Api, self).__init__(app, self.prefix, *args, **kwargs)

    def init_app(self, app):
        self.register_resources()
        super(Api, self).init_app(app)

    def register_resources(self):
        for resource, path in self.api_resources:
            if isinstance(path, tuple):
                self.add_resource(resource, *path)
            else:
                self.add_resource(resource, path)

    def add_resource(self, resource, *urls, **kwargs):
        if 'endpoint' not in kwargs:
            kwargs['endpoint'] = str('{prefix}__{resourse}').format(
                prefix=self.endpoint_prefix,
                resourse=resource.get_endpoint())
        return super(Api, self).add_resource(resource, *urls, **kwargs)

    def handle_error(self, e):
        result = None
        if isinstance(e, ResourceError):
            result = {'error': e.status,
                      'details': e.details}, e.code
        elif isinstance(e, ValidationError):
            result = {'error': 'validation_error',
                      'details': e.messages}, 400
        if result:
            return self.make_response(result[0], result[1])
        return super(Api, self).handle_error(e)
