from optparse import OptionParser
from bottle import Bottle

import threading, time
from queue import Queue

from ring_api.dring import Dring
from ring_api.restfulserver.server import BottleServer

def options():
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

    parser.add_option('-r', '--rest',
        action='store_true', dest='rest', default=False,
        help='start with restful server api')

    parser.add_option('--port',
        type='int', dest='port', default=8080,
        help='restful server port')

    parser.add_option('--host',
        type='str', dest='host', default='127.0.0.1',
        help='restful server host')

    return parser.parse_args()

class Client:

    def __init__(self, _options=None):
        self.dring = Dring()

        if not _options:
            (_options, args) = options()
        self.options = _options

        bitflags = self.options_to_bitflags(self.options)
        self.dring.init_library(bitflags)

        if self.options.version:
            print(self.dring.version())

        self.dring_thread = threading.Thread(target=self.dring.start)
        self.dring_thread.setDaemon(not self.options.persistent)

        if self.options.rest:
            self.restapp = BottleServer(
                    self.options.host, self.options.port, self.dring)
            self.restapp_thread = threading.Thread(target=self.restapp.start)

    def options_to_bitflags(self, options):
        flags = 0

        if options.console:
            flags |= self.dring.FLAG_CONSOLE_LOG

        if options.debug:
            flags |= self.dring.FLAG_DEBUG

        if options.autoanswer:
            flags |= self.dring.FLAG_AUTOANSWER

        return flags

    def start(self):
        """
            TODO:
                Better main loop control
                Do pj_thread_register() to exit ring gracefully
        """
        self._start_dring()
        # main loop choice
        if self.options.rest:
            time.sleep(3)
            self._start_restapp()
        else:
            q = Queue()
            while True:
                q.get()

    def _start_dring(self):
        self.dring_thread.start()

    # thread by default
    def _start_restapp(self):
        self.restapp_thread.start()

