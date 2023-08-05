# This file serves as an entry point to PIP that uses hardcoded "setup.py" script.
# For development when whole project is checked out, this file only builds the core subproject.
# It is advised to use setup_proxy.py and setup_gui.py explicitly.

# In case of PIP, only proxy or only gui is present in the egg file,
# so the failure to import the other one has to be silently ignored.

try:
    import setup_proxy
    exit(0)
except ImportError:
    pass

try:
    import setup_gui
    exit(0)
except ImportError:
    pass

raise Exception("The distribution must contain either http-proxy or http-proxy-gui subproject.")