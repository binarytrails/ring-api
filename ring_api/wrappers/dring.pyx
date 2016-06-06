# cython: language_level=3

from libcpp.string cimport string

from ring_api.utils.std cimport *
from ring_api.interfaces cimport dring
from ring_api.interfaces cimport configuration_manager as config_man

cdef class ConfigurationManager:
    def __cinit__(self):
        pass

    def accounts(self):
        accounts = list()
        raw_accounts = config_man.getAccountList()
        for i, account in enumerate(raw_accounts):
            accounts.append(account.decode())
        return accounts

    def account_details(self, str_id):
        cdef string b_id = str_id
        details = dict()
        raw_dict = config_man.getAccountDetails(b_id)
        for key in raw_dict.iterkeys():
            value = raw_dict[key]
            details[key] = value.decode()
        return details

cdef class Dring:
    cdef:
        readonly int FLAG_DEBUG
        readonly int FLAG_CONSOLE_LOG
        readonly int FLAG_AUTOANSWER

    cdef public ConfigurationManager config

    def __cinit__(self):
        self.FLAG_DEBUG          = dring.DRING_FLAG_DEBUG
        self.FLAG_CONSOLE_LOG    = dring.DRING_FLAG_CONSOLE_LOG
        self.FLAG_AUTOANSWER     = dring.DRING_FLAG_AUTOANSWER


        self.config = ConfigurationManager()
        if(not self.config):
            raise RuntimeError

    def init_library(self, bitflags=0):
        if(not dring.init(bitflags)):
            raise RuntimeError

        # register callbacks
        #cdef function[dring.CallbackWrapperBase] func;
        #ctypedef const map[string, SharedCallback] config_event_handlers
        #self.configuration_manager.registerConfHandlers(func)

    def start(self):
        if(not dring.start()):
            raise RuntimeError

    def version(self):
        return dring.version().decode()

