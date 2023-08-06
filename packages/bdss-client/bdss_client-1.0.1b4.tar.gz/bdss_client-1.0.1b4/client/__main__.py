# Big Data Smart Socket
# Copyright (C) 2016 Clemson University
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along
# with this program; if not, write to the Free Software Foundation, Inc.,
# 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
#

import argparse
import logging
import sys
import traceback

from colorlog import ColoredFormatter

from .actions import action_module, available_action_info


def main():
    parser = argparse.ArgumentParser(prog="bdss", description="BDSS client")

    parser.add_argument("--no-color", action="store_true", help="Produce monochrome output")

    parser.add_argument("--verbose", "-v", action="store_true", help="Produce verbose output")

    subparsers = parser.add_subparsers(dest="action",
                                       help="See `bdss <action> -h` to read about a specific action",
                                       metavar="action",
                                       title="available actions")

    for action, help_text in available_action_info():
        action_parser = subparsers.add_parser(action, help=help_text)
        action_module(action).configure_parser(action_parser)

    subparsers.add_parser("help", help="Show this help message and exit")

    args = parser.parse_args()

    logger = logging.getLogger("bdss")
    logger.setLevel(logging.INFO)

    handler = None
    if args.no_color:
        handler = logging.StreamHandler()
        handler.setFormatter(logging.Formatter("%(asctime)s %(levelname)s - %(message)s"))
    else:
        handler = logging.StreamHandler()
        handler.setFormatter(ColoredFormatter("%(log_color)s%(asctime)s %(levelname)s - %(message)s",
                             log_colors={
                                 'DEBUG':    'white',
                                 'INFO':     'cyan',
                                 'WARNING':  'yellow',
                                 'ERROR':    'red',
                                 'CRITICAL': 'red'
                             }))
    handler.setLevel(logging.DEBUG)
    logger.addHandler(handler)

    if args.verbose:
        logger.setLevel(logging.DEBUG)

    if not args.action or args.action == "help":
        parser.print_help(file=sys.stderr)
        sys.exit(0)

    try:
        action_module(args.action).handle_action(args, parser)
    except Exception as e:
        logger.error("Failed %s action" % args.action)
        logger.error(e)
        logger.debug(traceback.format_exc())
        sys.exit(1)

if __name__ == "__main__":
    main()
