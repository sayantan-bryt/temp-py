# Small scripts required 

## `adb_intg.py`

Primarily used for running adb shell commands exposed via an flask app for systems having not enough privilege.


## `mitm_addon.py`

To run the addon, have [mitmproxy](https://docs.mitmproxy.org/stable/overview-installation/) installed

``mitmweb --listen-port 9999 -s blocker_addon.py  --set ignore_hosts=".*firebase.*, .*google.*"``
