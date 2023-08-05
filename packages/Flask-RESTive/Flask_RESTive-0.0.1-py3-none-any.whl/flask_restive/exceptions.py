# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from werkzeug.exceptions import HTTPException


class ResourceError(HTTPException):
    description = 'Resource error'
    code = 500

    def __init__(self, details=None, description=None, code=None):
        if code is not None:
            self.code = code
        self.details = details or {}
        super(ResourceError, self).__init__(description)


class AccessDenied(ResourceError):
    description = 'Access denied to the resource'
    code = 403


class DoesNotExist(ResourceError):
    description = 'Resource does not exist'
    code = 404


class AlreadyExists(ResourceError):
    description = 'Resource already exists'
    code = 409


class TemporaryUnavailable(ResourceError):
    description = 'Resource temporary unavailable'
    code = 503
