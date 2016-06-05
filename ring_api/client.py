from optparse import OptionParser

from ring_api.dring import Dring
from ring_api.restfulserver.server import BottleServer


class Client:

    def __init__(self):
        self.dring = Dring()
        
        (options, args) = self._init_options()
        bitflags = self.options_to_bitflags(options)

        if options.version:
            print(self.dring.version())

        self.dring.init_library(bitflags)
 
        self.restserver = BottleServer('localhost', 8080, self.dring)

    def _init_options(self):
        usage = 'usage: %prog [options] arg1 arg2'
        parser = OptionParser(usage=usage)

        parser.add_option('-v', '--version',
            action='store_true', dest='version', default=False,
            help='show Ring-daemon version')

        parser.add_option('-d', '--debug',
            action='store_true', dest='debug', default=False,
            help='debug mode (more verbose)')

        parser.add_option('-c', '--console',
            action='store_true', dest='console', default=False,
            help='log in console (instead of syslog)')

        parser.add_option('-p', '--persistent',
            action='store_true', dest='persistent', default=False,
            help='stay alive after client quits')

        parser.add_option('--auto-answer',
            action='store_true', dest='autoanswer', default=False,
            help='force automatic answer to incoming call')

        return parser.parse_args()


    def options_to_bitflags(self, options):
        flags = 0

        if options.console:
            flags |= self.dring.FLAG_CONSOLE_LOG

        if options.debug:
            flags |= self.dring.FLAG_DEBUG

        if options.autoanswer:
            flags |= self.dring.FLAG_AUTOANSWER

        return flags

    def start_dring(self):
        self.dring.start()

    def start_restserver(self):
        self.restserver.start()

