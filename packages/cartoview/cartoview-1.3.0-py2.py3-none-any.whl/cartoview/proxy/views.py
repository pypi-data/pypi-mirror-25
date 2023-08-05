from __future__ import print_function
from __future__ import unicode_literals
from __future__ import division
from __future__ import absolute_import
from future import standard_library
standard_library.install_aliases()
from builtins import *
import requests
from django.http import HttpResponse
from django.http import QueryDict
from django.views.decorators.csrf import csrf_exempt

from django.conf import settings
urls = {
    'geoserver': settings.OGC_SERVER['default']['PUBLIC_LOCATION'],
}


def send_request(request, url, requests_args=None):
    requests_args = (requests_args or {}).copy()
    headers = get_headers(request.META)
    params = request.GET.copy()

    if 'headers' not in requests_args:
        requests_args['headers'] = {}
    if 'data' not in requests_args:
        requests_args['data'] = request.body
    if 'params' not in requests_args:
        requests_args['params'] = QueryDict('', mutable=True)

    # Overwrite any headers and params
    # from the incoming request with explicitly
    # specified values for the requests library.
    headers.update(requests_args['headers'])
    params.update(requests_args['params'])

    # If there's a content-length header from Django, it's probably in all-caps
    # and requests might not notice it, so just remove it.
    for key in list(headers.keys()):
        if key.lower() == 'content-length':
            del headers[key]

    requests_args['headers'] = headers
    requests_args['params'] = params
    # url = "https://ao82912.maps.arcgis.com" \
    # if url == "" else "https://ao82912.maps.arcgis.com/" + url
    print(url)
    response = requests.request(
        request.method, url, stream=True, **requests_args)

    proxy_response = HttpResponse(
        response.content, status=response.status_code)

    excluded_headers = set([
        # Hop-by-hop headers
        # ------------------
        # Certain response headers should NOT be just tunneled through.  These
        # are they.  For more info, see:
        # http://www.w3.org/Protocols/rfc2616/rfc2616-sec13.html#sec13.5.1
        'connection',
        'keep-alive',
        'proxy-authenticate',
        'proxy-authorization',
        'te',
        'trailers',
        'transfer-encoding',
        'upgrade',

        # Although content-encoding is not listed among the hop-by-hop headers,
        # it can cause trouble as well.  Just let the server set the value as
        # it should be.
        'content-encoding',

        # Since the remote server may or may not have sent the content in the
        # same encoding as Django will, let Django worry about what the length
        # should be.
        'content-length',
    ])
    for key, value in list(response.headers.items()):
        if key.lower() in excluded_headers:
            continue
        proxy_response[key] = value

    return proxy_response


@csrf_exempt
def proxy_view(request, url_name, sub_url, requests_args=None):
    url = urls[url_name] + sub_url
    return send_request(request, url, requests_args)


def get_headers(environ):
    """
    Retrieve the HTTP headers from a WSGI environment dictionary.  See
    https://docs.djangoproject.com/en/dev/ref/request-response/#django.http.HttpRequest.META
    """
    headers = {}
    for key, value in list(environ.items()):
        # Sometimes, things don't like when you send the requesting host
        # through.
        if key.startswith('HTTP_') and key != 'HTTP_HOST':
            headers[key[5:].replace('_', '-')] = value
        elif key in ('CONTENT_TYPE', 'CONTENT_LENGTH'):
            headers[key.replace('_', '-')] = value

    return headers
