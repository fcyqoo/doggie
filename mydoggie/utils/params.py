import json
import logging

from django.http import HttpResponse
from enum import IntEnum
from .exceptions import IllegalArgumentError

logger = logging.getLogger(__name__)


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def check_required_params(required_params, data_dict):
    for required_param in required_params:
        if required_param not in data_dict:
            raise IllegalArgumentError('Missing required parameter %s' % required_param)


def check_request(request, required_params=None, method='POST'):
    if required_params is None:
        required_params = []

    if request.method != method:
        raise IllegalArgumentError('HTTP method is wrong for %s: %s expected, %s is used.' % (request.path, method, request.method))

    if method == 'POST':
        data = request.POST
    elif method == 'GET':
        data = request.GET
    elif method == 'OPTIONS':
        data = {}
    else:
        raise IllegalArgumentError('We only support POST and GET at this point.')

    check_required_params(required_params, data)


def check_request_2(request_dict, required_params=None):
    if required_params is None:
        required_params = []

    check_required_params(required_params, request_dict)


def allow_cors(response, origin=None):
    allow_origin = ['http://localhost:8081', 'http://zvdev:8081', 'http://zenvideo.cn', 'http://localhost:8888', 'http://data.zenvideo.cn', 'http://www.ipmfj.com']
    if origin is not None and origin in allow_origin:
        response["Access-Control-Allow-Origin"] = origin
        response["Access-Control-Allow-Headers"] = origin
    else:
        response["Access-Control-Allow-Origin"] = "http://localhost:8081"
        response["Access-Control-Allow-Headers"] = "http://localhost:8081"
    response["Access-Control-Allow-Methods"] = "POST, GET, OPTIONS"
    response["Access-Control-Max-Age"] = "1000"
    response["Access-Control-Allow-Credentials"] = 'true'
    return response


def json_response(code, message, params={}, encoding='utf-8'):
    response = dict(code=int(code), message=message)
    for key in params:
        response[key] = params[key]
    return HttpResponse(json.dumps(response, skipkeys=True),
                        content_type='application/json;charset=%s' % encoding)


class ApiErrorCode(IntEnum):
    ok = 0,
    generic_error = 1,


def get_int_field(data, name, default=None, zero=True, neg=True, nullable=True):
    try:
        value = data.get(name, default)
        if default is None and value is None:
            if nullable:
                return None
            else:
                raise IllegalArgumentError('{} must not be null.'.format(name))
        else:
            value = int(value)

    except ValueError:
        raise IllegalArgumentError('%s must be in integer format' % name)

    if not neg and value < 0:
        raise IllegalArgumentError('%s must be non-negative' % name)
    if not zero and value == 0:
        raise IllegalArgumentError('%s must be non-zero' % name)

    return value


def get_float_field(data, name, default=None, min_value=None, max_value=None):
    try:
        value = data.get(name, default)
        if default is None and value is None:
            return None
        else:
            value = float(value)

    except ValueError:
        raise IllegalArgumentError('%s must be float' % name)

    if max_value is not None:
        value = min(max_value, value)
    if min_value is not None:
        value = max(min_value, value)

    return value


def get_int_value(value, name):
    try:
        value = int(value)
    except ValueError:
        if not value:
            raise IllegalArgumentError('%s must not be empty' % name)
        else:
            raise IllegalArgumentError('%s must be integer' % name)

    return value


def get_boolean_field(data, name, default=None):
    try:
        value = data.get(name, default)
        if value is not default:
            if str(value).lower() in ['1', 'true', 'yes']:
                value = True
            else:
                value = False

    except ValueError:
        raise IllegalArgumentError('%s must be boolean' % name)

    return value


def get_request_field(data, name, default=None):
    try:
        value = data.get(name, default)
        if default is None and value in [None, 'null']:
            return None
        else:
            return value
    except ValueError:
        raise IllegalArgumentError('%s must be string' % name)


def get_optional_json_string(optional_dict, type, item):
    try:
        if optional_dict is None:
            return None
        return json.dumps(optional_dict)
    except TypeError:
        logger.error("Unable to serialize the %s object for item:%s" % (type, item))
        return None
