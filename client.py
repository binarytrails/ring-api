#!/usr/bin/env python3

from optparse import OptionParser

from dring import Dring
import server

dring = Dring()

def init_options():
    usage = "usage: %prog [options] arg1 arg2"
    parser = OptionParser(usage=usage)

    parser.add_option("-v", "--version",
        action="store_true", dest="version", default=False,
        help="show Ring-daemon version")

    parser.add_option("-d", "--debug",
        action="store_true", dest="debug", default=False,
        help="debug mode (more verbose)")

    parser.add_option("-c", "--console",
        action="store_true", dest="console", default=False,
        help="log in console (instead of syslog)")

    parser.add_option("-p", "--persistent",
        action="store_true", dest="persistent", default=False,
        help="stay alive after client quits")

    parser.add_option("--auto-answer",
        action="store_true", dest="autoanswer", default=False,
        help="force automatic answer to incoming call")

    return parser.parse_args()

def options_to_bitflags(options):
    flags = 0

    if options.console:
        flags |= dring.FLAG_CONSOLE_LOG

    if options.debug:
        flags |= dring.FLAG_DEBUG

    if options.autoanswer:
        flags |= dring.FLAG_AUTOANSWER

    return flags

if __name__ == "__main__":
    (options, args) = init_options()
    bitflags = options_to_bitflags(options)

    if options.version:
        print(dring.version())

    dring.init_library(bitflags)

    server.startServer()
