
from __future__ import print_function
import hmac
import hashlib
import config
import connect_method


API_VERSIONPATH = '/v0'


connect = None
connect_config_value = config.get_config_prop('connect_method')
if connect_config_value == 'requests':
    connect = connect_method.RequestsConnectMethod()
elif connect_config_value == 'curl':
    connect = connect_method.CurlConnectMethod()
else:
    # Default to requests
    connect = connect_method.RequestsConnectMethod()


def _auth_headers(message):
    auth_config = config.get_auth_or_die()
    default_lease = auth_config.default_lease()
    sig = hmac.new(default_lease.secret_api_key, message,
                   digestmod=hashlib.sha256).hexdigest()
    headers = dict(Authorization='{user_id}:{sig}'.format(
        user_id=default_lease.user_id,
        sig=sig
    ))
    return headers


# API
# these functions do not print


def post_performance_monitor_data(table):
    tsv = '\n'.join(map(lambda row: '\t'.join(row), table))
    
    path = '{versionpath}/performance/monitordata'.format(
        versionpath=API_VERSIONPATH
    )
    headers = {
        'Content-Type': 'text/tab-separated-values'
    }
    headers.update(_auth_headers(path))
    uri = '{endpoint}{path}'.format(endpoint=config.get_server(), path=path)
    r = connect.post(uri, headers=headers, data=tsv)
    return (r.status_code, r.json())

