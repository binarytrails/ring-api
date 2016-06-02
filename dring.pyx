# cython: language_level=3

from enum import Enum

from libcpp.string cimport string

from pxd cimport dring
from pxd cimport configurationmanager_interface as confman

cdef class ConfigurationManager:

    def account_details(self, ringID):
        cdef string ringId = string(<bytes> ringID)
        return confman.getAccountDetails(ringId)

cdef class Dring:
    cdef:
        readonly int FLAG_DEBUG
        readonly int FLAG_CONSOLE_LOG
        readonly int FLAG_AUTOANSWER

    cdef public ConfigurationManager configuration_manager

    def __cinit__(self):
        self.FLAG_DEBUG          = dring.DRING_FLAG_DEBUG
        self.FLAG_CONSOLE_LOG    = dring.DRING_FLAG_CONSOLE_LOG
        self.FLAG_AUTOANSWER     = dring.DRING_FLAG_AUTOANSWER

        self.configuration_manager = ConfigurationManager()
        if(not self.configuration_manager):
            raise RuntimeError


    def init_library(self, bitflags):
        if(not dring.init(bitflags)):
            raise RuntimeError

        if(not dring.start()):
            raise RuntimeError

    def version(self):
        return dring.version().decode('UTF-8')

