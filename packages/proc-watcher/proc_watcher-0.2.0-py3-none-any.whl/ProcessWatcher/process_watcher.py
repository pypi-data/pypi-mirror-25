#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import logging
import sys
import time
from argparse import RawTextHelpFormatter

from .process import *

version = '0.2.0'


def watch_process(args):
    log_level = logging.WARNING if args.quiet else logging.INFO
    log_format = '%(asctime)s %(levelname)s: %(message)s' if args.log else '%(message)s'
    logging.basicConfig(format=log_format, level=log_level)
    comms = []

    if args.daemon:
        try:
            daemon = Daemon()
            daemon.daemon()
        except DaemonException as err:
            logging.error('Failed to start daemon:::' + err.msg)
            sys.exit(1)

    if args.email:
        try:
            from .communicate import email

            comms.append((email, {'to': args.email}))
        except ImportError:
            logging.exception('Failed to load email module. (required by --email)')
            sys.exit(1)

    if args.notify:
        exception_message = 'Failed to load Desktop Notification module. (required by --notify)'
        try:
            from .communicate import dbus_notify

            comms.append((dbus_notify, {}))
        except ImportError as err:
            if err.name == 'notify2':
                logging.error("{}\n 'notify2' python module not installed.\n"
                              " use pip install notify2"
                              " (you also need to install the python3-dbus system package)".format(exception_message))
            else:
                logging.exception(exception_message)
            sys.exit(1)
        except:
            logging.exception(exception_message)
            sys.exit(1)

    # dict of all the process watching objects pid -> ProcessByPID
    # items removed when process ends
    watched_processes = {}

    # Initialize processes from arguments, get metadata
    for pid in args.pid:
        try:
            if pid not in watched_processes:
                watched_processes[pid] = ProcessByPID(pid)

        except NoProcessFound as ex:
            logging.warning('No process with PID {}'.format(ex.pid))

    process_matcher = ProcessMatcher()
    new_processes = ProcessIDs()

    for pattern in args.command:
        process_matcher.add_command_wildcard(pattern)

    for regex in args.command_regex:
        process_matcher.add_command_regex(regex)

    # Initial processes matching conditions
    for pid in process_matcher.matching(new_processes):
        if pid not in watched_processes:
            watched_processes[pid] = ProcessByPID(pid)

    # Whether program needs to check for new processes matching conditions
    # Would a user ever watch for a specific PID number to recur?
    watch_new = args.watch_new and process_matcher.num_conditions > 0

    if not watched_processes and not watch_new:
        logging.warning('No processes found to watch.')
        sys.exit()

    logging.info('Watching {} processes:'.format(len(watched_processes)))
    for pid, process in watched_processes.items():
        logging.info(process.info())

    try:
        to_delete = []
        while True:
            time.sleep(args.interval)
            # Need to iterate copy since removing within loop.
            for pid, process in watched_processes.items():
                try:
                    running = process.check()
                    if not running:
                        to_delete.append(pid)

                        logging.info('Process stopped\n%s', process.info())

                        for comm, send_args in comms:
                            comm.send(process=process, **send_args)

                except:
                    logging.exception(
                        'Exception encountered while checking or communicating about process {}'.format(pid))

                    if pid not in to_delete:
                        # Exception raised in check(), queue PID to be deleted
                        to_delete.append(pid)

            if to_delete:
                for pid in to_delete:
                    del watched_processes[pid]

                to_delete.clear()

            if watch_new:
                for pid in process_matcher.matching(new_processes):
                    try:
                        watched_processes[pid] = p = ProcessByPID(pid)
                        logging.info('watching new process\n%s', p.info())

                    except:
                        logging.exception('Exception encountered while attempting to watch new process {}'.format(pid))

            elif not watched_processes:
                sys.exit()

    except KeyboardInterrupt:
        # Force command prompt onto new line
        print()


def parse_from_command_line():
    # Remember to update README.md after modifying
    parser = argparse.ArgumentParser(
        epilog='ProcessWatcher v{version} (https://github.com/KEDYY/process-watcher)'.format(version=version),
        formatter_class=RawTextHelpFormatter,
        description="""Watch a process and notify when it completes via various communication protocols.\    
[+] indicates the argument may be specified multiple times, for example:
%(prog)s -p 1234 4258 -c myapp* -crx "exec\d+" --email person1@domain.com  person2@someplace.com
""".format(version=version))

    parser.add_argument('-i', '--interval', help='how often to check on processes. (default: 1.0 seconds)',
                        type=float, default=1.0, metavar='SECONDS')

    commands = parser.add_argument_group('Processes can be watched')
    commands.add_argument('-p', '--pid', help='process ID(s) to watch [+]',
                          nargs='+',
                          type=int,
                          default=[])
    commands.add_argument('-c', '--command',
                          help='watch all processes matching the command name pattern. (shell-style wildcards) [+]',
                          action='append', default=[], metavar='COMMAND_PATTERN')
    commands.add_argument('-crx', '--command-regex',
                          help='watch all processes matching the command name regular expression. [+]',
                          action='append', default=[], metavar='COMMAND_REGEX')
    commands.add_argument('-w', '--watch-new', help='watch for new processes that match --command. '
                                                    '(run forever)', action='store_true')

    mutually_exclusive_group = parser.add_mutually_exclusive_group()
    mutually_exclusive_group.add_argument('-d', '--daemon',
                                          action='store_true',
                                          help='watch processes in daemon mode')
    mutually_exclusive_group.add_argument('-q', '--quiet',
                                          help="don't print anything to stdout except warnings and errors",
                                          action='store_true')

    group_front = mutually_exclusive_group.add_argument_group('front')

    group_front.add_argument('--log', help="log style output (timestamps and log level)", action='store_true')

    notify = parser.add_argument_group('Notification')
    notify.add_argument('--notify', help='send DBUS Desktop notification', action='store_true')
    notify.add_argument('--email', help='email address to send to [+]', nargs='+', metavar='EMAIL_ADDRESS')
    # Just print help and exit if no arguments specified.
    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit()

    return parser.parse_args()


def main():
    args = parse_from_command_line()
    watch_process(args)


if __name__ == '__main__':
    main()
