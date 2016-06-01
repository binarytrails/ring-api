# cython: language_level=3

from enum import Enum

from libcpp.string cimport string

from pxd cimport dring as dring
from pxd cimport configurationmanager_interface as confman

cdef class ConfigurationManager:

    def getAccountDetails(self, ringID):
        cdef string ringId = string(<bytes> ringID)
        return confman.getAccountDetails(ringId)

cdef class Dring:
    cdef:
        readonly DEBUG
        readonly CONSOLE_LOG
        readonly AUTOANSWER
        configurationManager

    def __cinit__(self):
        self.DEBUG          = dring.DRING_FLAG_DEBUG
        self.CONSOLE_LOG    = dring.DRING_FLAG_CONSOLE_LOG
        self.AUTOANSWER     = dring.DRING_FLAG_AUTOANSWER

        self.configurationManager = ConfigurationManager()
        if(not self.configurationManager):
            raise RuntimeError

        if(not dring.init(self.DEBUG)):
            raise RuntimeError

        if(not dring.start()):
            raise RuntimeError

        print(self.version())

        testRingID = str.encode('49c58c110d7aaa119b78b456cfebf1042a43f885')
        print(self.configurationManager.getAccountDetails(testRingID))

    def _initLibrary(self, flags):
        pass

    def version(self):
        return dring.version().decode('UTF-8')

