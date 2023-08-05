#!/usr/bin/env python3

import argparse
import os
import rollbar
import sys


SCRIPT_LOCATION = os.path.dirname(os.path.realpath(__file__))
ROOT_PATH = os.path.normpath(os.path.join(SCRIPT_LOCATION, '..'))
CONFIG_LOCATION = os.path.join(SCRIPT_LOCATION, 'logfit_config.yaml')
sys.path.append(ROOT_PATH)

from logfit import __version__
from logfit.client import LogFit
from logfit.config import Config


def main():
    rollbar.init(Config.ROLLBAR_TOKEN, Config.ROLLBAR_ENV)
    try:
        parse_args(sys.argv[1:])
    except KeyboardInterrupt:
        pass
    except Exception as e:
        rollbar.report_exc_info()
        raise


def parse_args(sys_args):
    parser = argparse.ArgumentParser(
        description='Read and upload log files to log.fit'
    )
    parser.add_argument(
        'command',
        choices=['start', 'run', 'foreground', 'stop', 'restart', 'status'],
    )
    parser.add_argument(
        '-v', '--version', action='version', version=__version__,
    )
    args = parser.parse_args(sys_args)
    config = Config()
    config.read_config_file(CONFIG_LOCATION)
    log_fit_client = LogFit(
        pidfile="/tmp/logfit.pid",
        config=config,
    )
    command = args.command
    if command == 'start':
        log_fit_client.start()
    elif command in ['run', 'foreground']:
        log_fit_client.run()
    elif command == 'stop':
        log_fit_client.stop()
    elif command == 'restart':
        log_fit_client.restart()
    elif command == 'status':
        log_fit_client.is_running()


if __name__ == '__main__':
    main()
