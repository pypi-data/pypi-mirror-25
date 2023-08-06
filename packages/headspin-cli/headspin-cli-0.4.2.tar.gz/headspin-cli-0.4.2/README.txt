# headspin-cli
CLI for the HeadSpin platform API.

Installation/Upgrade:
--
```
pip install --upgrade headspin-cli
```

Usage:
--
```
CLI for the HeadSpin platform API

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
```

Detailed Description:
--
```
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

```

Version History:
--

0.1
* Add device status to device listing.
* Add `device inspect`.

0.2
* Focus device listing on remote control devices.
* Add adb connect/disconnect/add-adb-keys functionality.
* Support switching between `requests` library and `curl`
  as the underlying method for speaking to the server.

0.3
* Introduce basic support for iOS devices
