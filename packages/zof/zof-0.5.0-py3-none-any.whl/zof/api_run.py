"""
Implements run() function.
"""

import sys
from .api_args import common_args
from .controller import Controller
from .logging import init_logging
from .pidfile import PidFile


def run(*, args=None):
    """Run event loop for zof.

    Args:
        args (Optional[argparse.Namespace]): Arguments derived from
            ArgumentParser. If None, use `common_args` parser. If args is a
            list, pass these to parse_args.
    """
    if args is None:
        args = common_args(include_x_modules=True).parse_args()
    elif isinstance(args, (list, tuple)):
        args = common_args(include_x_modules=True).parse_args(args)

    if args.loglevel:
        init_logging(args.loglevel, args.logfile)

    if args.x_uvloop:
        import uvloop  # pylint: disable=import-error
        import asyncio
        asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

    with PidFile(args.pidfile):
        controller = Controller.singleton()
        exit_status = controller.run_loop(args=args)

    if not args.x_under_test:
        sys.exit(exit_status)

    return exit_status
