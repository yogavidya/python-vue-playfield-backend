import sys, os
import inspect
import http
import re
from dotenv import load_dotenv
from flask import Flask, request, make_response
import json
from functools import reduce
from App.app_cors.functions import valid_origin, preflight_request_response
from App.type_info.functions import members_names, is_hashable, is_iterable
import logging
from . import logger

load_dotenv()

def _api_success(payload):
  if 'message' not in payload:
    payload['message'] = 'ready'
  response = make_response({'status': 'ok',
                      'data': payload})
  response.access_control_allow_origin = valid_origin()
  return response

def _api_error(payload, message='error', status=http.HTTPStatus.INTERNAL_SERVER_ERROR):
  payload['message'] = message
  response = make_response({'status': 'error',
                    'data': payload})
  response.status_code = status
  response.access_control_allow_origin = valid_origin()
  return response


def create_backend():
  logger.info('create_backend')
  rest_server = Flask(__name__, template_folder = '../templates')

  # GET / (Handshake route)
  @rest_server.route('/', methods=['GET'])
  def hello():
    return _api_success({})
  
  # GET /python_version
  @rest_server.route('/python-version', methods=['GET'])
  def python_version():
    return _api_success({'version': sys.version})

  # /python-eval preflight route
  @rest_server.route('/python-eval', methods=['OPTIONS'])
  def preflight_route():
    return preflight_request_response()

  # POST /python-eval
  @rest_server.route('/python-eval', methods=['POST'])
  def python_eval():
    payload = json.loads(request.data)
    if 'expression' in payload:
        try:
            result = eval(payload['expression'])
        except BaseException as exc:
            return _api_success({'exception': exc.args})
        else:
            return _api_success({'result': str(result),
                                'type': type(result).__name__,
                                'iterable': is_iterable(result),
                                'hashable': is_hashable(result),
                                'details': members_names(result)})
    else:
        return _api_error({})

  return rest_server


if __name__ == "__main__":
  logger.debug('***** Starting backend')
  backend = create_backend()
  backend.run()