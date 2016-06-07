from optparse import OptionParser
from bottle import Bottle

import threading, time
from queue import Queue

from ring_api.dring import Dring
from ring_api.restfulserver.server import BottleServer

def options():
    usage = 'usage: %prog [options] arg1 arg2'
    parser = OptionParser(usage=usage)

    parser.add_option('-v', '--verbose',
        action='store_true', dest='verbose', default=False,
        help='activate all of the verbose options')

    parser.add_option('-d', '--debug',
        action='store_true', dest='debug', default=False,
        help='debug mode (more verbose)')

    parser.add_option('-c', '--console',
        action='store_true', dest='console', default=False,
        help='log in console (instead of syslog)')

    parser.add_option('-p', '--persistent',
        action='store_true', dest='persistent', default=False,
        help='stay alive after client quits')

    parser.add_option('-r', '--rest',
        action='store_true', dest='rest', default=False,
        help='start with restful server api')

    parser.add_option('--port',
        type='int', dest='port', default=8080,
        help='restful server port')

    parser.add_option('--host',
        type='str', dest='host', default='127.0.0.1',
        help='restful server host')

    parser.add_option('--auto-answer',
        action='store_true', dest='autoanswer', default=False,
        help='force automatic answer to incoming call')

    parser.add_option('--dring-version',
        action='store_true', dest='dring_version', default=False,
        help='show Ring-daemon version')

    parser.add_option('--realtime',
        action='store_true', dest='realtime', default=False,
        help='adapt threads for real-time interaction')

    return parser.parse_args()

class Client:

    def __init__(self, _options=None):
        self.dring = Dring()

        if (not _options):
            (_options, args) = options()
        self.options = _options

        if (self.options.verbose):
            self.options.debug = True
            self.options.console = True

        bitflags = self.options_to_bitflags(self.options)
        self.__init_threads__(bitflags)

        if (self.options.dring_version):
            print(self.dring.version())

    def __init_threads__(self, bitflags):
        self.dring.init_library(bitflags)
        self.dring_thread = threading.Thread(target=self.dring.start)
        self.dring_thread.setDaemon(not self.options.persistent)

        if (self.options.rest):
            self.restapp = BottleServer(
                    self.options.host, self.options.port, self.dring)
            self.restapp_thread = threading.Thread(target=self.restapp.start)

        if (self.options.realtime):
            self.mother_thread = threading.Thread(target=self._start_main_loop)

    def options_to_bitflags(self, options):
        flags = 0

        if (options.console):
            flags |= self.dring._FLAG_CONSOLE_LOG

        if (options.debug):
            flags |= self.dring._FLAG_DEBUG

        if (options.autoanswer):
            flags |= self.dring._FLAG_AUTOANSWER

        return flags

    def start(self):
        try:
            if (self.options.realtime):
                self.mother_thread.start()
            else:
                self._start_main_loop()

        except (KeyboardInterrupt, SystemExit):
            self.stop()

    def _start_main_loop(self):
        self.dring_thread.start()

        if (self.options.rest):
            time.sleep(3)
            self.restapp_thread.start()

        while True:
            time.sleep(0.1)
            self.dring.poll_events()

    def stop(self):
        if (self.options.verbose):
            print("Finishing..")

        self.dring.stop()

        if hasattr(self, 'restapp'):
            self.restapp.stop()

