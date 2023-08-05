# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from werkzeug.exceptions import HTTPException


class ResourceError(HTTPException):
    description = 'Resource error'
    status = 'resource_error'
    code = 500

    def __init__(self, details=None, status=None, description=None, code=None):
        if status is not None:
            self.status = status
        if code is not None:
            self.code = code
        self.details = details or {}
        super(ResourceError, self).__init__(description)


class AccessDenied(ResourceError):
    description = 'Access denied to the resource'
    status = 'resource_access_denied'
    code = 403


class DoesNotExist(ResourceError):
    description = 'Resource does not exist'
    status = 'resource_does_not_exist'
    code = 404


class AlreadyExists(ResourceError):
    description = 'Resource already exists'
    status = 'resource_already_exists'
    code = 409
