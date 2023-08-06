#!/usr/bin/env python

"""CLI for the HeadSpin platform API

Usage:
  hs (-h | --help)
  hs auth init <token> [-v]
  hs auth ls
  hs auth set-default <credentials_number>
  hs session ls [<num_sessions>] [-a] [--json] [-v]
  hs session inspect <session_uuid> [--writefiles] [--json] [-v]
  hs session start [network_container|capture] <device_id> [--json] [-v]
  hs session stop <session_uuid> [--json] [-v]
  hs session mar <session_uuid> [-v]
  hs session har <session_uuid> [-v]
  hs device ls [<selector>] [--json] [-v]
  hs device connect <selector> [--json] [-v]
  hs device disconnect <selector> [--json] [-v]
  hs device lock <selector> [--json] [-v]
  hs device unlock <selector> [--json] [-v]
  hs device keys [--json] [-v]
  hs config add-adb-key [--path=<adb_key_path>] [--json] [-v]
  hs config server [<server>]
  hs config connect-method [(requests|curl)]
  hs appium url <device_id> [-t <api_token>]
  hs appium lock-url <device_id> [-t <api_token>]
  hs appium unlock-url <device_id> [-t <api_token>]
  hs sign <path> [--json] [--curl]


Detailed Description:

  Note: The --json flag dumps the raw JSON output as returned by the
  sever. The -v flag turns on verbose logging in the requests library,
  showing the HTTP requests and responses (headers-only).

  Some commands accept a <selector> argument. A <selector> is a json string
  of key, value pairs that match device attributes. For example:

        hs device ls '{ "manufacturer": "motorola" }'
        hs device lock '{ "serial": "XSNC43" }'

  Use `hs device keys` to see a list of keys you can use in a selector,
  and `hs device ls --json` to see some possible values for those keys.


  hs auth init <token>

        Authorizes this device given a one-time token <token>. Contact
        support@headspin.io to request an authorization token.

  hs auth ls

        Prints the current credentials.

  has auth set-default <credentials_number>

        Sets the credentials number <credentials_number> as the default.
        The numbering can be seen via the `hs auth info` command.

  hs session ls [<num_sessions>] [-a]

        Outputs a list of session metadata in reverse-chronological
        order. <num_sessions> is the number of sessions output, 5 by
        default. By default only active sessions are output. The `-a`
        flag will cause inactive sessions to be inclued in the result.

  hs session inspect <session_uuid> [--writefiles]

        Outputs details for a session given the session's UUID. If
        `--writefiles` is given, data associated with session endpoints
        is written to files.

  hs session start network_container <device_id>

        Starts a HeadSpin network container session on a device
        specified by <device_id>. The container's default network
        interface (eth0) is on the device's mobile network. The container
        can be accessed via SSH login. In addition, a device can access
        the remote mobile network by connecting to a VPN.

  hs session start capture <device_id>

        Starts video capture on a device specified by <device_id>. End
        capture with the `hs session stop` command.

  hs session stop <session_uuid>

        Stops a session in progress.

  hs session mar <session_id>

        Downloads the captured network traffic from a HeadSpin session
        in HeadSpin's MAR format. MAR is a HAR-like JSON format that
        contains the data in a network capture at a high level.

  hs session har <session_id>

        Downloads the captured network traffic from a HeadSpin session
        in HAR format.

  hs device ls [<selector>]

        Lists all devices, optionally matching a selector.

  hs device connect <selector> [--json]

        Connect a remote device locally. For Android, an `adb connect`
        is performed. The first device that matches the selector is used.

  hs device disconnect <selector> [--json]

        Disconnect all devices matched by the selector.

  hs device lock <selector> [--json]

        Lock the first device that matches the selector.

  hs device unlock <selector> [--json]

        Unlock all devices matched by the selector.

  hs device keys [--json]

        List keys that can be used in a <selector>, as in
        `hs device connect <selector>` or `hs device disconnect <selector>`.

  hs config add-adb-key [--path=<adb_key_path>] [--json]

        Add an adb key to all remote control hosts. If a path is not
        specified, ~/.android/adbkey.pub is used.

  hs config server <server>

        Set the HeadSpin API server URL.

  hs config connect-method [(requests|curl)]

        Set the method by which requests are issued to the server. The
        "requests" method uses the python requests library. The "curl"
        method uses command-line curl.

  hs appium url <device_id> [-t <api_token>]

        Retrieves the appium url to use for running an appium test on
        the given device. The api token is currently required, and
        can be retrieved from the UI in the user settings menu. The url
        will end with /wd/hub

  hs appium lock-url <device_id> [-t <api_token>]

        Retrieves the appium url to lock the given device. Similar to
        'appium url', the api token is currently required.

  hs appium unlock-url <device_id> [-t <api_token>]

        Retrieves the appium url to unlock the given device. Similar to
        'appium url', the api token is currently required.

"""

from __future__ import print_function
import sys
import urllib
import os
import time
import json
import datetime
import traceback
import subprocess
import termcolor
from docopt import docopt
import config

from api import (API_VERSIONPATH, connect, _auth_headers)


def auth_init(token):
    """Authorizes the device with a one-time token."""
    uri = '{endpoint}{versionpath}/auth'.format(
        versionpath=API_VERSIONPATH,
        endpoint=config.get_server()
    )
    r = connect.post(uri, data=json.dumps(dict(auth_token=token)))
    if r.status_code != 200:
        print(json.dumps(r.json(), indent=2))
        return

    response_body = r.json()
    config.add_leases(response_body['leases'])


def auth_ls():
    auth_config = config.get_auth_or_die()
    print('Credentials:')
    for i, lease in enumerate(auth_config.leases):
        default = ''
        if i == auth_config.default_lease_index:
            default = '*'
        print(' {default:2} {num}. {org} {role}'.format(
            default=default,
            num=str(i+1),
            org=lease.org_title,
            role='/ {0}'.format(lease.role)
            if lease.role is not None else ''
        ))


def auth_setdefault(lease_number):
    auth_config = config.get_auth_or_die()
    try:
        num = int(lease_number)-1
        assert auth_config.leases[num] is not None
        auth_config.default_lease_index = num
        auth_config.write()
    except:
        print('Bad credentials number')
        os._exit(1)


def format_timedelta(ts1, ts2):
    delta = (datetime.datetime.fromtimestamp(ts2) -
             datetime.datetime.fromtimestamp(ts1))
    hours, remainder = divmod(delta.seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    if hours == 0 and minutes == 0:
        return '{0:3} second{1} ago'.format(seconds, '' if seconds == 1 else 's')
    elif hours == 0:
        return '{0:3} minute{1} ago'.format(minutes, '' if minutes == 1 else 's')
    else:
        return '{0:3} hour{1} ago'.format(hours, '' if hours == 1 else 's')


def session_ls(num_sessions=5, include_all=False, as_json=False):
    """List sessions. If num_sessions == 0, list all active sessions.  If
    num_sessions > 0, list the last `num_sessions` sessions, active or
    not.
    """
    # note: the path is used as the message to sign
    path = '{versionpath}/sessions?{params}'.format(
        versionpath=API_VERSIONPATH,
        params=urllib.urlencode(dict(
            num_sessions=num_sessions,
            include_all=include_all
        ))
    )
    uri = '{endpoint}{path}'.format(
        endpoint=config.get_server(),
        path=path
    )
    r = connect.get(uri, headers=_auth_headers(path))
    body = r.json()
    if r.status_code != 200 or as_json:
        print(json.dumps(body, indent=2))
        return

    fmt_string = ("{session_id:40}  {session_type:15}  {state:10}  " +
                  "{start_time:30}  {device_id:<20}")
    print(fmt_string.format(
        session_id='Session ID',
        session_type='Type',
        state='State',
        start_time='Start Time',
        device_id='Device IMEI'
    ))

    for session in body['sessions']:
        print(fmt_string.format(
            session_id=session['session_id'],
            session_type=session['session_type'],
            state=session['state'],
            start_time=time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(
                session['start_time'])),
            device_id=session['device_id']
        ))


def session_start(session_type, device_id,
                  companion_id=None, as_json=False):
    """Start session. `session_type` can be one of "http_proxy",
    "network_container", "device_container", or "capture". If companion_id is
    given, network capture will be turned on. If the companion_id is None,
    network capture can be optionally turned on.
    """
    path = '{versionpath}/sessions'.format(versionpath=API_VERSIONPATH)
    uri = '{endpoint}{path}'.format(
        endpoint=config.get_server(),
        path=path
    )
    r = connect.post(uri, headers=_auth_headers(path), data=json.dumps(dict(
        device_id=device_id,
        session_type=session_type,
        companion_id=companion_id
    )))

    response = r.json()

    if r.status_code != 200 or as_json:
        print(json.dumps(r.json(), indent=2))
        return

    session_id = response['session_id']
    print('Session ID:', session_id)

    if 'endpoints' not in response:
        return

    endpoints = response['endpoints']

    for endpoint in endpoints:
        if endpoint['type'] == 'ssh':
            host = endpoint['host']
            port = endpoint['port']
            private_key = endpoint['credentials']['private_key']
            private_key_filename = session_id + '.key'
            with open(private_key_filename, 'w') as pkey_file:
                pkey_file.write(private_key)
            os.chmod(private_key_filename, 0400)
            print('SSH Host/Port: {host}:{port}'.format(host=host, port=port))
            print('SSH Private Key:', private_key_filename)
            print('Log into container:')
            print('')
            print('\tssh -i {key} ubuntu@{host} -p {port}'.format(
                key=private_key_filename,
                host=host,
                port=port))
            print('')

        if endpoint['type'] == 'http_proxy':
            host = endpoint['host']
            port = endpoint['port']
            print('Proxy Host/Port: {host}:{port}'.format(host=host, port=port))
            print('Example HTTP requests using curl:')
            print('')
            print('\tcurl -x {host}:{port} www.imdb.com'.format(
                host=host, port=port))
            print('')

        if endpoint['type'] == 'ovpn':
            host = endpoint['host']
            port = endpoint['port']
            client_ovpn = endpoint['credentials']['client_config']
            client_ovpn_filename = session_id + '.ovpn'
            with open(client_ovpn_filename, 'w') as ovpn_file:
                ovpn_file.write(client_ovpn)
            print('OpenVPN Server Host/Port: {host}:{port}'.format(host=host, port=port))
            print('OpenVPN Config:', client_ovpn_filename)
            print('')


def session_inspect(session_id, as_json=False, write_files=False):
    """Print details about a session."""
    path = '{versionpath}/sessions/{id}'.format(
        versionpath=API_VERSIONPATH,
        id=session_id
    )
    uri = '{endpoint}{path}'.format(endpoint=config.get_server(), path=path)
    r = connect.get(uri, headers=_auth_headers(path))

    body = r.json()

    if r.status_code != 200 or as_json:
        print(json.dumps(body, indent=2))
        return

    print('Session ID:  ', body['session_id'])
    print('Type:        ', body['session_type'])
    print('State:       ', body['state'])
    print('Start Time:  ', time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(
        body['start_time'])))
    print('Device ID:   ', body['device_id'])
    print('')
    print('Endpoints:')
    print('')
    for i, e in enumerate(body['endpoints']):
        print('{i}.'.format(i=i+1))
        print('  Host: ', e['host'])
        print('  Port: ', e['port'])
        if e['type'] == 'ssh':
            print('  Type:  SSH')
            print('  User:  ubuntu')
            if write_files:
                filename = body['session_id'] + '.key'
                try:
                    with open(filename, 'w') as out:
                        out.write(e['credentials']['private_key'])
                    os.chmod(filename, 0400)
                    print('  Private key written:', filename)
                except IOError:
                    print('  Key file exists:', filename)
        if e['type'] == 'http_proxy':
            print('  Type:  HTTP Proxy')
        if e['type'] == 'ovpn':
            print('  Type:  OpenVPN')
            if write_files:
                filename = body['session_id'] + '.ovpn'
                with open(filename, 'w') as out:
                    out.write(e['credentials']['client_config'])
                print('  Client config written:', filename)


def session_stop(session_id, as_json):
    """Stop a session in progress."""
    path = '{versionpath}/sessions/{id}'.format(
        versionpath=API_VERSIONPATH,
        id=session_id
    )
    uri = '{endpoint}{path}'.format(endpoint=config.get_server(), path=path)
    r = connect.patch(uri, headers=_auth_headers(path),
                      data=json.dumps(dict(active=False)))
    body = r.json()
    if r.status_code != 200 or as_json:
        print(json.dumps(body, indent=2))
        return
    print('Stopped')
    if 'msg' in body:
        print(body.get('msg'))


def session_data(session_id, data_type):
    """Dump the data from a session. data_type can be either "mar" or
    "har".
    """
    path = '{versionpath}/sessions/{id}/{data_type}'.format(
        versionpath=API_VERSIONPATH,
        id=session_id,
        data_type=data_type
    )
    uri = '{endpoint}{path}'.format(endpoint=config.get_server(), path=path)
    r = connect.get(uri, headers=_auth_headers(path))
    print(json.dumps(r.json(), indent=2))


def _get_status_text(device):
    status_text = device['status_text']
    status_reason = device['status_reason']
    if status_text not in ['Healthy', 'Unknown', 'Busy']:
        status_text = status_reason
    return status_text


def device_ls(selector=None, as_json=False):
    """List devices for this org."""

    selectors = [] if selector is None else parse_selector(selector)

    path = '{versionpath}/devices'.format(versionpath=API_VERSIONPATH)
    params = urllib.urlencode([('selector', s) for s in selectors])
    if params != '':
        path += '?{0}'.format(params)
    uri = '{endpoint}{path}'.format(
        endpoint=config.get_server(),
        path=path
    )
    r = connect.get(uri, headers=_auth_headers(path))
    body = r.json()

    if r.status_code != 200 or as_json:
        print(json.dumps(body, indent=2))
        return

    fmt_string = ("{hostname:30} {device_type:10}  {device_id:40}  {serial:20}  {operator:20}  {connection:10}  "
                  + "{status:12}  {companion:10} {in_use:20} {last_update:10}")

    print(fmt_string.format(
        hostname='Hostname',
        device_type='Type',
        device_id='Device ID',
        serial='Serial',
        operator='Operator',
        connection='Connection',
        status='Status',
        companion='Companion',
        in_use='In Use',
        last_update='Last Update'
    ))

    sorted_devices = sorted(
        body['devices'],
        key=lambda d: (d['hostname']
                       + (d['phone_network'] or '')
                       + (d['operator'] or ''))
    )

    now = time.time()

    def device_status(device):
        # https://github.com/projectxyzio/stf/blob/master/res/app/components/stf/device/enhance-device/enhance-device-service.js#L4-L36
        # https://github.com/projectxyzio/web/blob/master/ui.headspin.io/src/services/device-list-svc.js#L71-L107
        try:
            state = 'unavailable'
            device_dict = device['device']
            if not device['removed']:
                if device_dict['present']:
                    if device_dict['status'] == 1:
                        state = 'offline'
                    elif device_dict['status'] == 2:
                        state = 'unauthorized'
                    elif device_dict['status'] == 3:
                        state = 'preparing'
                        if device_dict['ready']:
                            state = 'ready'
                            if device_dict['owner']:
                                state = 'busy'
                if device['device_type'] == 'ios' and device_dict.get('blocked'):
                    state = 'blocked'
            return state
        except:
            return '-'

    for device in sorted_devices:
        status_time = format_timedelta(device['timestamp'], now)
        status_text = device_status(device)
        print(fmt_string.format(
            hostname=device['hostname'],
            device_type=device['device_type'],
            device_id=device['device_id'],
            serial=device['serial'],
            imei=device['phone_imei'],
            operator=device['operator'],
            connection=device['phone_network'] if device['device_type'] == 'android' else 'n/a',
            status=status_text,
            companion='Yes' if device['is_companion_device'] else 'No',
            in_use=(device['device']['owner']['email']
                    if device['device']['owner'] else '-'),
            last_update=status_time
        ))


def parse_selector(selector):
    try:
        with open(os.path.expanduser(selector), 'r') as f:
            selector = f.read()
    except:
        pass
    return [selector]


def device_connect(selector, as_json):
    """Lock a device and get its adb connect url"""
    selectors = parse_selector(selector)
    path = '{versionpath}/devices?{params}'.format(
        versionpath=API_VERSIONPATH,
        params=urllib.urlencode([('selector', s) for s in selectors])
    )
    uri = '{endpoint}{path}'.format(endpoint=config.get_server(), path=path)
    r = connect.post(uri, headers=_auth_headers(path))
    body = r.json()

    if r.status_code != 200:
        print(json.dumps(body, indent=2))
        return

    if as_json:
        print(json.dumps(body, indent=2))
    else:
        print(body['hostname'], ' ', body['serial'])

    subprocess.call('adb connect {url}'.format(
        url=body['adb_connect_url']
    ), shell=True)


def device_disconnect(selector, as_json):
    """Unlock a device and disconnect from adb"""
    selectors = parse_selector(selector)
    path = '{versionpath}/devices?{params}'.format(
        versionpath=API_VERSIONPATH,
        params=urllib.urlencode([('selector', s) for s in selectors])
    )
    uri = '{endpoint}{path}'.format(endpoint=config.get_server(), path=path)
    r = connect.delete(uri, headers=_auth_headers(path))
    body = r.json()

    if r.status_code != 200 or as_json:
        print(json.dumps(body, indent=2))
        return

    fmt_string = '{hostname:30} {serial:20} {status:10} {message}'
    print(fmt_string.format(
        hostname='Hostname',
        serial='Serial',
        status='Status',
        message='Message'
    ))
    for s in body['statuses']:
        l = fmt_string.format(
            hostname=s['hostname'],
            serial=s['serial'],
            status='Success' if s['success'] else 'Fail',
            message=s.get('message')
        )
        if s['success']:
            print(l)
        else:
            print(termcolor.colored(l, 'red'))


def device_lock(selector, as_json):
    """Locks the first device that matches the selector."""
    selectors = parse_selector(selector)
    path = '{versionpath}/devices/lock?{params}'.format(
        versionpath=API_VERSIONPATH,
        params=urllib.urlencode([('selector', s) for s in selectors])
    )
    uri = '{endpoint}{path}'.format(endpoint=config.get_server(), path=path)
    r = connect.post(uri, headers=_auth_headers(path))
    body = r.json()

    if r.status_code != 200 or as_json:
        print(json.dumps(body, indent=2))
        return

    print(body['status'])


def device_unlock(selector, as_json):
    """Unlock all devices that match the selector."""
    selectors = parse_selector(selector)
    path = '{versionpath}/devices/lock?{params}'.format(
        versionpath=API_VERSIONPATH,
        params=urllib.urlencode([('selector', s) for s in selectors])
    )
    uri = '{endpoint}{path}'.format(endpoint=config.get_server(), path=path)
    r = connect.delete(uri, headers=_auth_headers(path))
    body = r.json()

    if r.status_code != 200 or as_json:
        print(json.dumps(body, indent=2))
        return

    fmt_string = '{hostname:30} {device_id:40} {status:10} {message}'
    print(fmt_string.format(
        hostname='Hostname',
        device_id='Device ID',
        status='Status',
        message='Message'
    ))
    for s in body['statuses']:
        l = fmt_string.format(
            hostname=s['hostname'],
            device_id=s['device_id'],
            status='Success' if s['success'] else 'Fail',
            message=s['message']
        )
        if s['success']:
            print(l)
        else:
            print(termcolor.colored(l, 'red'))


def device_keys(as_json):
    """Print keys that can be used in a device <selector>"""
    path = '{versionpath}/devices/keys'.format(versionpath=API_VERSIONPATH)
    uri = '{endpoint}{path}'.format(endpoint=config.get_server(), path=path)
    r = connect.get(uri, headers=_auth_headers(path))
    body = r.json()

    if r.status_code != 200 or as_json:
        print(json.dumps(body, indent=2))
        return

    for key in body['keys']:
        print(key)


def config_add_adb_key(adb_key_path, as_json):
    """Add an adb_key to this user's hosts"""
    if adb_key_path is None:
        adb_key_path = '~/.android/adbkey.pub'
    try:
        with open(os.path.expanduser(adb_key_path), 'r') as f:
            adb_key = f.readline()
    except:
        print('Failed to read key from {0}'.format(adb_key_path))
        return

    path = '{versionpath}/user/adbkeys'.format(versionpath=API_VERSIONPATH)
    uri = '{endpoint}{path}'.format(endpoint=config.get_server(), path=path)
    r = connect.post(uri, headers=_auth_headers(path), data=json.dumps(dict(
        adb_key=adb_key
    )))

    body = r.json()

    if r.status_code != 200 or as_json:
        print(json.dumps(body, indent=2))
        return

    for host, result in body.iteritems():
        print('{host}: {result}'.format(host=host, result=result))


def config_set_server(server):
    if server is None:
        print(config.get_server())
    else:
        config.set_config_prop('server', server)


def config_set_connect_method(method):
    if method is None:
        print(config.get_config_prop('connect_method'))
    else:
        config.set_config_prop('connect_method', method)


def sign(path, as_json, as_curl_opts):
    headers = _auth_headers(path)
    if as_curl_opts:
        args = []
        for header, value in headers.iteritems():
            args.extend([
                '-H ',
                '"{header}: {value}"'.format(header=header, value=value)
            ])
        print(' '.join(args))
    elif as_json:
        print(json.dumps(headers, indent=2))
    else:
        for header, value in headers.iteritems():
            print('{header}\t{value}'.format(
                header=header,
                value=value
            ))


def _appium_get_data(device_id, field, api_token):
    if api_token is None:
        print("API Token must be given, use -t <api_token>")
        return None
    path = '{endpoint}{versionpath}/devices/automation-config'.format(
        versionpath=API_VERSIONPATH,
        endpoint=config.get_server())
    if api_token is None:
        headers = _auth_headers(path)
    else:
        headers = {'Authorization': 'Bearer {api_token}'.format(
            api_token=api_token)}

    #print(headers)

    #print(path)

    response = connect.get(path, headers=headers)
    #print(json)

    body = response.json()

    if response.status_code != 200:
        print(json.dumps(body, indent=2))
        return None

    if device_id in body:
        return body[device_id][field].format(api_token=api_token)
    else:
        print("error: {device_id} was not found".format(device_id=device_id))
        return None


def appium_get_url(device_id, api_token = None):
    driver_url = _appium_get_data(device_id, 'driver_url', api_token)
    if driver_url is not None:
        print(driver_url)


def appium_get_lock_url(device_id, api_token = None):
    url = _appium_get_data(device_id, 'lock_url', api_token)
    if url is not None:
        print(url)


def appium_get_unlock_url(device_id, api_token = None):
    url = _appium_get_data(device_id, 'unlock_url', api_token)
    if url is not None:
        print(url)


def main(args):
    args = docopt(__doc__, version='HeadSpin CLI v0.2.1', argv=args)

    def cli(cmd):
        flags = [args[part] for part in cmd.split(' ')]
        return reduce(lambda x, y: x and y, flags)

    def session_type():
        if 'http_proxy' in args and args['http_proxy']:
            return 'http_proxy'
        if 'network_container' in args and args['network_container']:
            return 'network_container'
        if 'device_container' in args and args['device_container']:
            return 'device_container'
        if 'capture' in args and args['capture']:
            return 'capture'

    if args['-v']:
        connect.verbose()

    auth_token = None
    if args['-t']:
        auth_token = args['<api_token>']

    if cli('auth init'):
        auth_init(args['<token>'])
    if cli('auth ls'):
        auth_ls()
    if cli('auth set-default'):
        auth_setdefault(args['<credentials_number>'])
    if cli('session ls'):
        try:
            num_sessions = int(args['<num_sessions>'])
            session_ls(
                num_sessions=num_sessions,
                include_all=args['-a'],
                as_json=args['--json']
            )
        except:
            session_ls(include_all=args['-a'], as_json=args['--json'])
    if cli('session inspect'):
        session_inspect(args['<session_uuid>'], args['--json'],
                        args['--writefiles'])
    if cli('session start'):
        session_start(session_type(),
                      args['<device_id>'],
                      None,
                      args['--json'])
    if cli('session stop'):
        session_stop(args['<session_uuid>'], args['--json'])
    if cli('session har'):
        session_data(args['<session_uuid>'], 'har')
    if cli('session mar'):
        session_data(args['<session_uuid>'], 'mar')
    if cli('device ls'):
        device_ls(args['<selector>'], args['--json'])
    if cli('device connect'):
        device_connect(args['<selector>'], args['--json'])
    if cli('device disconnect'):
        device_disconnect(args['<selector>'], args['--json'])
    if cli('device lock'):
        device_lock(args['<selector>'], args['--json'])
    if cli('device unlock'):
        device_unlock(args['<selector>'], args['--json'])
    if cli('device keys'):
        device_keys(args['--json'])
    if cli('config add-adb-key'):
        config_add_adb_key(args['--path'], args['--json'])
    if cli('config server'):
        config_set_server(args['<server>'])
    if cli('appium lock-url'):
        appium_get_lock_url(args['<device_id>'], auth_token)
    if cli('appium unlock-url'):
        appium_get_unlock_url(args['<device_id>'], auth_token)
    if cli('appium url'):
        appium_get_url(args['<device_id>'], auth_token)
    if cli('config connect-method'):
        if args['requests']:
            method = 'requests'
        elif args['curl']:
            method = 'curl'
        else:
            method = None
        config_set_connect_method(method)
    if cli('sign'):
        sign(
            args['<path>'],
            args['--json'],
            args['--curl']
        )


def console_main():
    try:
        main(sys.argv[1:])
    except SystemExit:
        raise
    except:
        traceback.print_exc()
        print('An error has occurred. Try updating the headspin-cli package:\n')
        print('\tpip install --upgrade headspin-cli\n')
        print('If the problem persists, contact HeadSpin at support@headspin.io.')

if __name__ == '__main__':
    console_main()
