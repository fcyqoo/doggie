from django.shortcuts import render

import logging
from django.views.decorators.csrf import csrf_exempt
from utils.exceptions import IllegalArgumentError
from utils.params import json_response, ApiErrorCode, get_int_field, get_boolean_field
from utils.view_wapper import handle_api_request
from .manager import dao


@csrf_exempt
@handle_api_request(required_args=[], method='GET')  # todo： change to post in the future
def wiki_index(request, request_dict, timer):

    return json_response(ApiErrorCode.ok, 'ok')


@csrf_exempt
@handle_api_request(required_args=[], method='GET')  # todo： change to post in the future
def update_dog_base(request, request_dict, timer):
    dao.do_update()
    return json_response(ApiErrorCode.ok, 'ok')


@csrf_exempt
@handle_api_request(required_args=[], method='GET')  # todo： change to post in the future
def update_dog_info(request, request_dict, timer):
    path = 'dogwiki/data/info.json'
    data = dao.read_json(path)

    dao.do_update_info(data)
    return json_response(ApiErrorCode.ok, 'ok')


