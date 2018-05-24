import sys
import pprint
import logging

from django.http import HttpResponse
from django.http import HttpResponseBadRequest, HttpResponseServerError
from django.http import HttpResponseForbidden
from django.conf import settings

from .exceptions import IllegalArgumentError, ExceptionWithErrorCode, UnauthorizedException, ForbiddenException
from .params import check_request, allow_cors, json_response, check_request_2
from .timer import SimpleTimer

import warnings
import functools
import traceback

logger = logging.getLogger('api')


def handle_task(task_desc=None):
    def wrap(task_method):

        def add_timer(*args, **kwargs):
            log_task_desc = task_desc
            if log_task_desc is None:
                log_task_desc = task_method.__name__

            timer = SimpleTimer(log_task_desc, kwargs)

            try:
                task_method(timer, *args, **kwargs)
            except Exception as e:
                logger.exception('Exception running task %s: %s' % (log_task_desc, e))
            finally:
                timer.finish()

        return add_timer

    return wrap


def handle_api_request_auth(required_args=None, method='POST', api_desc=None):
    if required_args is None:
        required_args = []

    def wrap(view_func):
        def handle_exceptions(request):
            origin = request.environ.get('HTTP_ORIGIN')
            timer = None
            try:
                if request.method == 'OPTIONS':
                    response = HttpResponse()
                    response['allow'] = ','.join([method, 'OPTIONS'])
                    return allow_cors(response, origin)

                if method == 'POST':
                    request_dict = request.POST
                else:
                    request_dict = request.GET

                log_api_desc = api_desc
                if log_api_desc is None:
                    log_api_desc = view_func.__name__

                if 'user_id' in request_dict:
                    user_id = request_dict['user_id']
                elif request.user.is_authenticated():
                    user_id = request.user.pk
                else:
                    raise ForbiddenException

                timer = SimpleTimer(log_api_desc, request_dict)

                check_request_2(request_dict, required_args)
                response = view_func(request, request_dict, user_id, timer)

                return allow_cors(response, origin)

            except IllegalArgumentError as e:
                log_api_desc = api_desc
                if log_api_desc is None:
                    log_api_desc = view_func.__name__
                logger.exception('Illegal argument handing request %s: %s' % (log_api_desc, e.message))
                return allow_cors(HttpResponseBadRequest(content=e.message), origin)

            except ExceptionWithErrorCode as e:
                log_api_desc = api_desc
                if log_api_desc is None:
                    log_api_desc = view_func.__name__
                logger.exception('System Exception handling request %s: %s' % (log_api_desc, e.message))
                return allow_cors(json_response(e.err_code, e.message), origin)

            except ForbiddenException as e:
                logger.error('Forbidden Exception handling request %s: %s' % (log_api_desc, e.message))
                return allow_cors(HttpResponseForbidden(content=e.message), origin)

            except Exception as e:
                traceback.print_exc()
                log_api_desc = api_desc
                if log_api_desc is None:
                    log_api_desc = view_func.__name__
                _, _, tb = sys.exc_info()
                tb_locals = []
                while tb:
                    tb_locals.append(pprint.pformat(tb.tb_frame.f_locals))
                    tb = tb.tb_next
                msg = '\n\n'.join(tb_locals)
                logger.exception("Exception handling request %s: %s%s%s" %
                                 (log_api_desc, e.message, settings.EMAIL_SUBJECT_SEPARATOR, msg))
                return allow_cors(HttpResponseServerError(
                    content='Sorry, our service is experiencing some issues. Please try again later.'), origin)

            finally:
                if timer is not None:
                    timer.finish()

        return handle_exceptions

    return wrap


def handle_api_request(required_args=None, method='POST', api_desc=None, require_auth=False):
    if required_args is None:
        required_args = []

    def wrap(view_func):
        def handle_exceptions(request):

            origin = request.environ.get('HTTP_ORIGIN')
            timer = None
            try:
                if method == 'POST':
                    request_dict = request.POST
                elif method == 'OPTIONS':
                    request_dict = {}
                else:
                    request_dict = request.GET

                log_api_desc = api_desc
                if log_api_desc is None:
                    log_api_desc = view_func.__name__

                timer = SimpleTimer(log_api_desc, request_dict)

                if require_auth and not request.user.is_authenticated():
                    raise ForbiddenException

                check_request(request, required_args, method)
                response = view_func(request, request_dict, timer)

                return allow_cors(response, origin)

            except IllegalArgumentError as e:
                log_api_desc = api_desc
                if log_api_desc is None:
                    log_api_desc = view_func.__name__
                logger.exception('Illegal argument handing request %s: %s' % (log_api_desc, e.message))
                return allow_cors(HttpResponseBadRequest(content=e.message), origin)

            except ExceptionWithErrorCode as e:
                log_api_desc = api_desc
                if log_api_desc is None:
                    log_api_desc = view_func.__name__
                logger.exception('System Exception handling request %s: %s' % (log_api_desc, e.message))
                return allow_cors(json_response(e.err_code, e.message), origin)

            except ForbiddenException as e:
                logger.error('Forbidden Exception handling request %s: %s' % (log_api_desc, e.message))
                return allow_cors(HttpResponseForbidden(content=e.message), origin)

            except Exception as e:
                log_api_desc = api_desc
                if log_api_desc is None:
                    log_api_desc = view_func.__name__
                logger.exception("Exception handling request %s: %s" % (log_api_desc, e.message))
                return allow_cors(HttpResponseServerError(
                    content='Sorry, our service is experiencing some issues. Please try again later.'), origin)

            finally:
                if timer is not None:
                    timer.finish()

        return handle_exceptions

    return wrap


def handle_view(required_args=[], method='GET', api_desc=None, log_error=True):
    def wrap(view_func):
        def handle_exceptions(request):

            timer = None
            origin = request.environ.get('HTTP_ORIGIN')
            try:
                if method == 'POST':
                    request_dict = request.POST
                else:
                    request_dict = request.GET

                log_api_desc = api_desc
                if log_api_desc is None:
                    log_api_desc = view_func.__name__

                timer = SimpleTimer(log_api_desc, request_dict)

                check_request(request, required_args, method)
                response = view_func(request, request_dict, timer)

                return allow_cors(response, origin)

            except IllegalArgumentError as e:
                log_api_desc = api_desc
                if log_api_desc is None:
                    log_api_desc = view_func.__name__
                if log_error:
                    logger.exception('Illegal argument handing request %s: %s' % (log_api_desc, e.message))
                return allow_cors(HttpResponseBadRequest(content=e.message))

            except ExceptionWithErrorCode as e:
                log_api_desc = api_desc
                if log_api_desc is None:
                    log_api_desc = view_func.__name__
                if log_error:
                    logger.exception('Exception handling request %s: %s' % (log_api_desc, e.message))
                return allow_cors(json_response(e.err_code, e.message), origin)

            except UnauthorizedException as e:
                return allow_cors(HttpResponse(status=401, content=e.message), origin)

            except Exception as e:
                log_api_desc = api_desc
                if log_api_desc is None:
                    log_api_desc = view_func.__name__
                if log_error:
                    logger.exception("Exception handling request %s: %s" % (log_api_desc, e.message))
                return allow_cors(HttpResponseServerError(
                    content='Sorry, our service is experiencing some issues. Please try again later: %s' % e.message))

            finally:
                if timer is not None:
                    timer.finish()

        return handle_exceptions

    return wrap


def deprecated(func):
    """This is a decorator which can be used to mark functions
    as deprecated. It will result in a warning being emmitted
    when the function is used."""

    @functools.wraps(func)
    def new_func(*args, **kwargs):
        warnings.simplefilter('always', DeprecationWarning)  # turn off filter
        warnings.warn("Call to deprecated function {}.".format(func.__name__), category=DeprecationWarning,
                      stacklevel=2)
        warnings.simplefilter('default', DeprecationWarning)  # reset filter
        return func(*args, **kwargs)

    return new_func
