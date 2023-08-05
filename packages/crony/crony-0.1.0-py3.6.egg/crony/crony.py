# -*- coding: utf-8 -*-
"""Here's the beef."""
import argparse
import configparser
import getpass
import logging
import subprocess
import os
import sys

import raven
import requests
from raven.handlers.logging import SentryHandler

__version__ = "0.1.0"

CONFIG = None
LOGGER = logging.getLogger('crony')
OPTS = None
SENTRY_CLIENT = None


def cronitor(cmd):
    """Wrap run with requests to cronitor."""
    url = f'https://cronitor.link/{OPTS.cronitor}/{{}}'

    try:
        run_url = url.format('run')
        LOGGER.debug(f'Pinging {run_url}')
        requests.get(run_url, timeout=OPTS.timeout)

    except requests.exceptions.RequestException as e:
        LOGGER.exception(e)

    # Cronitor may be having an outage, but we still want to run our stuff
    complete = run(cmd, OPTS)

    endpoint = 'complete' if complete.returncode == 0 else 'fail'
    try:
        ping_url = url.format(endpoint)
        LOGGER.debug('Pinging {}'.format(ping_url))
        requests.get(ping_url, timeout=OPTS.timeout)

    except requests.exceptions.RequestException as e:
        LOGGER.exception(e)

    return complete


def load_config():
    """Attempt to load config from file.

    User's come directory takes precedence over a system wide config.
    Config file in the user's dir should be named ".cronyrc".
    System wide config should be located at "/etc/crony.conf"
    """
    CONFIG = configparser.ConfigParser()

    home = os.path.expanduser('~{}'.format(getpass.getuser()))
    home_conf_file = os.path.join(home, '.cronyrc')
    system_conf_file = '/etc/crony.conf'

    conf_precedence = (home_conf_file, system_conf_file)
    for conf_file in conf_precedence:
        if os.path.exists(conf_file):
            CONFIG.read(conf_file)
            return f'Loading config from file {conf_file}.'


def log(complete):
    """Log given CompletedProcess and return exit status code."""
    if complete.stdout:
        LOGGER.info(complete.stdout)

    if complete.stderr:
        LOGGER.error(complete.stderr)

    return complete.returncode


def run(cmd):
    """Run command and report errors to Sentry."""
    LOGGER.debug(f'Running command: {cmd}')
    return subprocess.run(cmd, shell=True, stderr=subprocess.PIPE, stdout=subprocess.PIPE)


def setup_logging():
    """Setup python logging handler."""
    date_format = '%Y-%m-%dT%H:%M:%S'
    log_format = '%(asctime)s %(levelname)s: %(message)s'

    if OPTS.verbose:
        lvl = logging.DEBUG
    else:
        lvl = logging.INFO
        # Requests is a bit chatty
        logging.getLogger('requests').setLevel('WARNING')

    LOGGER.setLevel(lvl)

    stdout = logging.StreamHandler(sys.stdout)
    stdout.setLevel(lvl)
    formatter = logging.Formatter(log_format, date_format)
    stdout.setFormatter(formatter)
    LOGGER.addHandler(stdout)

    stderr = logging.StreamHandler(sys.stderr)
    stderr.setLevel(logging.ERROR)  # Error and above go to both stdout & stderr
    formatter = logging.Formatter(log_format, date_format)
    stderr.setFormatter(formatter)
    LOGGER.addHandler(stderr)

    if OPTS.log:
        logfile = logging.FileHandler(OPTS.log)
        logfile.setLevel(lvl)
        formatter = logging.Formatter(log_format, date_format)
        logfile.setFormatter(formatter)
        LOGGER.addHandler(logfile)

    if SENTRY_CLIENT:
        sentry = SentryHandler(SENTRY_CLIENT)
        sentry.setLevel(logging.ERROR)
        LOGGER.addHandler(sentry)

    LOGGER.debug('Logging setup complete.')


def main():
    """Entry point for running crony.

    1. If a --cronitor/-c is specified, a "run" ping is sent to cronitor.
    2. The argument string passed to crony is ran.
    3. Next steps depend on the exit code of the command ran.
        * If the exit status is 0 and a --cronitor/-c is specified, a "complete" ping is sent
            to cronitor.
        * If the exit status is greater than 0, a message is sent to Sentry with the output
            captured from the script's exit.
        * If the exit status is great than 0 and --cronitor/-c is specified, a "fail" ping
            is sent to cronitor.
    """
    parser = argparse.ArgumentParser(
        description='Monitor your crons with cronitor.io & sentry.io',
        epilog='https://github.com/youversion/crony',
        prog='crony'
    )

    parser.add_argument('-c', '--cronitor', action='store',
                        help='Cronitor link identifier. This can be found in your Cronitor unique'
                        ' ping URL right after https://cronitor.link/')

    parser.add_argument('-e', '--venv', action='store',
                        help='Path to virtualenv to source before running script. May be passed'
                        ' as an argument or loaded from an environment variable.')

    parser.add_argument('-d', '--cd', action='store',
                        help='If the script needs ran in a specific directory, than can be passed'
                        ' or cd can be ran prior to running crony.')

    parser.add_argument('-l', '--log', action='store',
                        help='Log file to direct stdout & stderr of script run to.')

    parser.add_argument('-p', '--path', action='store',
                        help='Paths to append to the PATH environment variable before running.')

    parser.add_argument('-s', '--dsn', action='store',
                        help='Sentry DSN. May be passed or loaded from an environment variable.')

    parser.add_argument('-t', '--timeout', action='store', default=10, help='Timeout to use when'
                        ' sending requests to Cronitor or Sentry', type=int)

    parser.add_argument('-v', '--verbose', action='store_true', help='Increase level of verbosity'
                        ' output by crony')

    parser.add_argument('cmd', nargs=argparse.REMAINDER, help='Command to run and monitor')

    OPTS = parser.parse_args()

    # Load system wide options from config file
    config_msg = load_config()

    # Setup Sentry Client before logging for SentryHandler
    if not OPTS.dsn:
        dsn = os.environ.get('SENTRY_DSN')
        if not dsn and CONFIG:
            dsn = CONFIG.get('SENTRY_DSN')
    else:
        dsn = OPTS.dsn
    if dsn:
        try:
            SENTRY_CLIENT = raven.Client(dsn)  # noqa
        except:
            sentry_success = True
        else:
            sentry_success = False

    setup_logging()

    # Now that logging is setup
    if config_msg:
        LOGGER.info(config_msg)
    if dsn and not sentry_success:
        LOGGER.error(f'Error connecting to Sentry: {dsn}')

    cmd = OPTS.cmd

    if OPTS.cd:
        LOGGER.debug(f'Adding cd to {OPTS.cd}')
        cmd = ['cd', OPTS.cd, '&&'] + cmd

    venv = OPTS.venv
    if not venv:
        venv = os.environ.get('CRONY_VENV')
    if venv:
        LOGGER.debug(f'Adding sourcing virtualenv {venv}')
        cmd = ['source', venv, '&&'] + cmd

    if OPTS.path:
        LOGGER.debug(f'Adding {OPTS.path} to PATH environment variable')
        cmd = ['export', f'PATH={OPTS.path}:$PATH', '&&'] + cmd

    if OPTS.cronitor:
        func = cronitor
    else:
        func = run

    sys.exit(log(func(cmd)))
