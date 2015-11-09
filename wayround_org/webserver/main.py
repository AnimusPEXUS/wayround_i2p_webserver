#!/usr/bin/python3

import sys
# import gc

# gc.set_debug(gc.DEBUG_LEAK)
# import pprint

# print("{}".format(pprint.pformat(sys.path)))

del sys.path[0]

import logging

import wayround_org.utils.program

wayround_org.utils.program.logging_setup(loglevel='INFO')

import wayround_org.webserver.commands

commands = wayround_org.webserver.commands.commands()

ret = wayround_org.utils.program.program('wrows', commands, None)

exit(ret)
