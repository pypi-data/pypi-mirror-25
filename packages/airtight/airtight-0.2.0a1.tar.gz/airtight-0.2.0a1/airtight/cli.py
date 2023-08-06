#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Easily initialize logging level and command-line arguments for a script.
"""
from airtight.logging import configure_logging
import argparse
import inspect
import logging
import sys


def configure_commandline(
        optional_arguments, positional_arguments, default_log_level):
    """Define and parse command line arguments

    Keyword arguments:
    optional_arguments -- a list of lists; each internal list defines an
        optional argument:
            short name (str)
            long name (str)
            default value,
            help string (str),
            required? (boolean)
    positional_arguments -- a list of lists; each internal list defines a
        positional argument:
            name (str)
            type (python type like "str", "int")
            help string (str)
    default_log_level -- an importance/severity level as defined by the Python
        "logging" module (e.g., logging.DEBUG, logging.INFO)
    """
    frame = inspect.currentframe().f_back
    module = inspect.getmodule(frame)
    parser = argparse.ArgumentParser(
        description=inspect.getdoc(module),
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    for a in optional_arguments:
        d = {
            'help': a[3],
            'required': a[4]
        }
        if type(a[2]) == bool:
            if a[2] is False:
                d['action'] = 'store_true'
                d['default'] = False
            else:
                d['action'] = 'store_false'
                d['default'] = True
        else:
            d['type'] = type(a[2])
            d['default'] = a[2]
        parser.add_argument(
            a[0],
            a[1],
            **d)
    for a in positional_arguments:
        d = {
            'type': a[1],
            'help': a[2]
        }
        parser.add_argument(a[0], **d)
    args = parser.parse_args()
    configure_logging(args, default_log_level)
    logging.debug('command line: {}'.format(' '.join(sys.argv)))
    return vars(args)
