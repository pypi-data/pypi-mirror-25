LogFit Daemon
=============

|PyPI| |Python Versions|

|Codeship Status for albertyw/logfit-daemon|

The LogFit daemon watches log files and sends data to the LogFit app
for analysis.

Installation
------------

TODO

Usage
-----

.. code:: bash

    # Start in foreground mode
    python3 logfit/client.py [run|foreground]

    # Start in daemon mode
    python3 logfit/client.py start

    # Stop daemon
    python3 logfit/client.py stop

    # Restart the daemon
    python3 logfit/client.py restart

    # Get the daemon status
    python3 logfit/client.py status


Configuration
-------------

The daemon can read from a ``logfit_config.yaml`` config file of the format:

.. code:: yaml

    # Required: Get this from your log.fit account
    source: "64a4b9bd88f14511926e0de86f23e2d8"

    # Optional: The directory the daemon will watch
    watch_directory: "/var/log/"

    # Optional: Minimum log level.  Possible options are
    # critical, error, warning, info, and debug
    log_level: "warning"

    # Optional: File to write daemon logs to
    log_file: "logfit.log"

    # Optional: limit watching log files to given mime types
    allowed_mime_types:
    - text/plain
    - inode/x-empty

    # Optional: List of file globs to not watch, should be the
    # full absolute path
    ignore_paths: []


Development
-----------

.. code:: bash

    pip install -r requirements-test.txt
    coverage run setup.py test
    coverage report
    flake8


Publishing
----------

.. code:: bash

    # Publish to PyPI
    python setup.py sdist bdist_wheel
    twine upload dist/*

    # Generate binaries for multiple operating systems
    pyinstaller logfit/main.py -F -p logfit --hidden-import queue -n logfit_linux_x86_64
    pyinstaller logfit/main.py -F -p logfit --hidden-import queue -n logfit_macos_x86_64
    pyinstaller logfit/main.py -F -p logfit --hidden-import queue -n logfit_windows_x86_64

    # Copy binaries into logfit-daemon-binary


.. |PyPI| image:: https://img.shields.io/pypi/v/logfit.svg
   :target: https://pypi.python.org/pypi/logfit/
.. |Python Versions| image:: https://img.shields.io/pypi/pyversions/logfit.svg
   :target: https://github.com/albertyw/logfit-daemon
.. |Codeship Status for albertyw/logfit-daemon| image:: https://app.codeship.com/projects/30a05060-4276-0135-97f1-6255c2e8e3ba/status?branch=master
   :target: https://app.codeship.com/projects/230349
