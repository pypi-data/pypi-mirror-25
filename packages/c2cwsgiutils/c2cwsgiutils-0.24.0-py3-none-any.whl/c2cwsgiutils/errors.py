"""
Install exception views to have nice JSON error pages.
"""
from cornice import cors
import logging
import os
from pyramid.httpexceptions import HTTPException
from pyramid.view import view_config
import sqlalchemy.exc
import traceback

DEVELOPMENT = os.environ.get('DEVELOPMENT', '0')

LOG = logging.getLogger(__name__)
STATUS_LOGGER = {
    400: LOG.info,
    401: LOG.info,
    500: LOG.error
    # The rest are warnings
}


def _crude_add_cors(request):

    response = request.response
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = \
        ','.join({request.headers.get('Access-Control-Request-Method', request.method)} | {'OPTIONS', 'HEAD'})
    response.headers['Access-Control-Allow-Headers'] = "session-id"
    response.headers['Access-Control-Max-Age'] = "86400"


def _add_cors(request):
    services = request.registry.cornice_services
    if request.matched_route is not None:
        pattern = request.matched_route.pattern
        service = services.get(pattern, None)
        if service is not None:
            request.info['cors_checked'] = False
            return cors.apply_cors_post_request(service, request, request.response)
    _crude_add_cors(request)


@view_config(context=HTTPException, renderer="json", http_cache=0)
def http_error(exception, request):
    log = STATUS_LOGGER.get(exception.status_code, LOG.warning)
    log("%s %s returned status code %s: %s",
        request.method, request.url, exception.status_code, str(exception),
        extra={'referer': request.referer})
    if request.method != 'OPTIONS':
        request.response.status_code = exception.status_code
        _add_cors(request)
        return {"message": str(exception), "status": exception.status_code}
    else:
        _crude_add_cors(request)
        request.response.status_code = 200


@view_config(context=sqlalchemy.exc.IntegrityError, renderer="json", http_cache=0)
def integrity_error(exception, request):
    return _do_error(request, 400, exception)


@view_config(context=ConnectionResetError, renderer="json", http_cache=0)
def client_interrupted_error(exception, request):
    # No need to cry wolf if it's just the client that interrupted the connection
    return _do_error(request, 500, exception, logger=LOG.info)


@view_config(context=Exception, renderer="json", http_cache=0)
def other_error(exception, request):
    return _do_error(request, 500, exception)


def _do_error(request, status, exception, logger=LOG.error):
    logger("%s %s returned status code %s: %s",
           request.method, request.url, status, str(exception),
           extra={'referer': request.referer}, exc_info=True)
    request.response.status_code = status
    _add_cors(request)
    response = {"message": str(exception), "status": status}

    if DEVELOPMENT != '0':
        trace = traceback.format_exc()
        response['stacktrace'] = trace
    return response
