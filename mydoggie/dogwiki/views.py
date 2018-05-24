from django.shortcuts import render

import logging
from django.views.decorators.csrf import csrf_exempt
from utils.exceptions import IllegalArgumentError
from utils.params import json_response, ApiErrorCode, get_int_field, get_boolean_field
from utils.view_wapper import handle_api_request


@csrf_exempt
@handle_api_request(required_args=[], method='GET')  # todo： change to post in the future
def wiki_index(request, request_dict, timer):

    return json_response(ApiErrorCode.ok, 'ok')


