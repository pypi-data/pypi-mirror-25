from __future__ import print_function
from tempfile import NamedTemporaryFile
import json
import subprocess
import requests
import logging


class Response(object):
    def __init__(self, status_code, json):
        self.status_code = status_code
        self._json = json

    def json(self):
        return self._json


def curl_request(method, uri, headers={}, data=None, verbose=False):
    headers = ' '.join([
        '-H "{name}: {value}"'.format(name=name, value=value)
        for name, value in headers.iteritems()
    ])
    if data is not None:
        data = "-d '{data}'".format(data=data)
    else:
        data = ''
    with NamedTemporaryFile() as output_file:
        cmd = 'curl 2>/dev/null -X {method} -w "%{{http_code}}" -o {fname} "{uri}" {headers} {data}'.format(
            method=method,
            fname=output_file.name,
            uri=uri,
            headers=headers,
            data=data
        )
        if verbose:
            print('Curl Command: {0}'.format(cmd))
        proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
        http_code_str, err = proc.communicate()
        if proc.returncode != 0:
            print(proc.returncode, err)
            raise ValueError('Could not execute curl command.')
        body_txt = output_file.read()
        if verbose:
            print('Return Code: {0}'.format(http_code_str))
            print('Return Body: {0}'.format(body_txt))
        body = json.loads(body_txt)
        return Response(int(http_code_str), body)


class CurlConnectMethod(object):
    def __init__(self):
        self._verbose = False

    def get(self, uri, headers={}):
        return curl_request('GET', uri, headers=headers,
                            verbose=self._verbose)

    def post(self, uri, headers={}, data=None):
        return curl_request('POST', uri, headers=headers, data=data,
                            verbose=self._verbose)

    def patch(self, uri, headers={}, data=None):
        return curl_request('PATCH', uri, headers=headers, data=data,
                            verbose=self._verbose)

    def delete(self, uri, headers={}):
        return curl_request('DELETE', uri, headers=headers,
                            verbose=self._verbose)

    def verbose(self):
        self._verbose = True


class RequestsConnectMethod(object):
    def __init__(self):
        pass

    def get(self, uri, headers={}):
        r = requests.get(uri, headers=headers)
        return Response(r.status_code, r.json())

    def post(self, uri, headers={}, data=None):
        r = requests.post(uri, headers=headers, data=data)
        return Response(r.status_code, r.json())

    def patch(self, uri, headers={}, data=None):
        r = requests.patch(uri, headers=headers, data=data)
        return Response(r.status_code, r.json())

    def delete(self, uri, headers={}):
        r = requests.delete(uri, headers=headers)
        return Response(r.status_code, r.json())

    def verbose(self):
        try:  # for Python 3
            from http.client import HTTPConnection
        except ImportError:
            from httplib import HTTPConnection
            HTTPConnection.debuglevel = 1
            logging.basicConfig()
            logging.getLogger().setLevel(logging.DEBUG)
            requests_log = logging.getLogger("requests.packages.urllib3")
            requests_log.setLevel(logging.DEBUG)
            requests_log.propagate = True
