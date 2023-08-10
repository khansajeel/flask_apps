from . import routes
import flask
import logging
import time
import random
from flask import request
from routes.polling_funcs import Polling

logger = logging.getLogger('polling_app')

def write_api_logs(request, response):
    url = request.url
    method = request.method
    if method == 'POST':
        data = str(request.data)
    else:
        data = str(request.args)
    logger.info("'url':'{}', 'data':'{}', 'success':'True'".format(url, data))
    if not response.get('success'):
        logger.info("'url':'{}', 'data':'{}', 'success':'False','error':'{}".format(url, data, str(response.get('error_info').get("message"))))


@routes.route('/healthcheck', methods=['GET'])
def health_check():
    return flask.jsonify('{}'), 200


@routes.route('/test', methods=['GET'])
def print_hello():
    final_result = dict()
    final_result.setdefault('success', True)
    try:
        headers = request.headers
        request_uid = headers.get('X-Unique-ID','')
        if request_uid == "":
            now = time.time()
            request_uid = 'polling_req' + str(int(now)) + '_' + str(int(random.random()*1000000))
        final_result['rsp_id'] = request_uid
        result = dict()
        result = Polling().print_hello()
    except Exception as e:
        final_result['success'] = False
        error_info = {
            'message': str(e),
        }
        final_result['error_info'] = error_info

    if final_result['success']:
        final_result['result'] = result
    write_api_logs(request, final_result)

    if final_result['success']:
        return flask.jsonify(final_result), 200
    else:
        return flask.jsonify(final_result), 400

