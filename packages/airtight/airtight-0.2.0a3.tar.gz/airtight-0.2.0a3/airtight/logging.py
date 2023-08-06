#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Easily configure logging for a script
"""

import inspect
import logging
import sys


def configure_logging(args, default=logging.WARNING):
    """Set logging levels based on defaults and command-line arguments

    Keyword arguments:
    args -- an argparse.Namespace object that may contain one or more of the
            following arguments:
                loglevel -- a severity/importance level from "logging"
                verbose -- True = logging.INFO is the desired level
                veryverbose -- True = logging.DEBUG is the desired level
    default -- a severity/importance level from the logging module that is to
               be used as the default logging level; it may be overridden by
               values provided in "args."
    """
    if args.loglevel is not 'NOTSET':
        args_log_level = ''.join(args.loglevel.upper().split())
        try:
            log_level = getattr(logging, args_log_level)
        except AttributeError:
            logging.error(
                'command line option to set log_level failed '
                'because {} is not a valid level name; using {}'
                ''.format(args_log_level, logging.getLevelName(default)))
            log_level = default
    elif args.veryverbose:
        log_level = logging.DEBUG
    elif args.verbose:
        log_level = logging.INFO
    else:
        log_level = default
    logging.basicConfig(level=log_level)
    if log_level != default:
        logging.info(
            'logging level changed to {} via command line option; was {}'
            ''.format(
                logging.getLevelName(log_level),
                logging.getLevelName(default)))
    else:
        logging.info(
            'using default logging level: {}'
            ''.format(logging.getLevelName(default)))


def flog(var, level=logging.DEBUG, comment=None):
    """Easily log a variable's name and value

    Keyword arguments:
    var -- the variable to log
    level -- the desired severity/importance level from the logging module
    comment -- an optional comment to postfix to the logged output
    """
    logger = logging.getLogger(sys._getframe(1).f_code.co_name)
    callers_local_vars = inspect.currentframe().f_back.f_locals.items()
    names = [
        var_name for var_name, var_val in callers_local_vars if var_val is var]
    if len(names) > 0:
        msg = '{}: {}'.format(names[0], repr(var))
    else:
        msg = ' {}'.format(repr(var))
    if comment is not None:
        msg = ''.join((comment, msg))
    logger.log(level, msg)

