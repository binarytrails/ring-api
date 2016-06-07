# cython: language_level=3

# Keep the logic of the interfaces
# Apply the logical partitioning in the API layer

from libcpp.string cimport string
from libcpp.map cimport map as map

from ring_api.utils.std cimport *
from ring_api.interfaces cimport dring
from ring_api.interfaces cimport configuration_manager as config_man

cdef class ConfigurationManager:
    def __cinit__(self):
        pass

    def accounts(self):
        """List user accounts (not ring ids)"""
        accounts = list()
        raw_accounts = config_man.getAccountList()

        for i, account in enumerate(raw_accounts):
            accounts.append(account.decode())

        return accounts

    def account_details(self, account_id):
        """Gets account details

        Keyword arguments:
        account_id -- account id string
        """
        cdef string raw_id = account_id.encode()
        details = dict()
        raw_dict = config_man.getAccountDetails(raw_id)

        for key, value in raw_dict.iteritems():
            details[key.decode()] = value.decode()

        return details

    def send_text_message(self, account_id, ring_id, content_map):
        """Sends a text message

        Keyword arguments:
        account_id  -- account id string
        ring_id     -- ring id destination string
        content_map -- map of content defined as [<mime-type>, <message>]
        """
        cdef string raw_account_id = account_id.encode()
        cdef string raw_ring_id = ring_id.encode()
        cdef map[string, string] raw_content_map

        for key, value in content_map.iteritems():
            raw_content_map[key.encode()] = value.encode()

        config_man.sendAccountTextMessage(
                raw_account_id, raw_ring_id, raw_content_map)

cdef class Dring:
    cdef:
        readonly int _FLAG_DEBUG
        readonly int _FLAG_CONSOLE_LOG
        readonly int _FLAG_AUTOANSWER

    cdef public ConfigurationManager config

    def __cinit__(self):
        self._FLAG_DEBUG          = dring.DRING_FLAG_DEBUG
        self._FLAG_CONSOLE_LOG    = dring.DRING_FLAG_CONSOLE_LOG
        self._FLAG_AUTOANSWER     = dring.DRING_FLAG_AUTOANSWER

        self.config = ConfigurationManager()
        if (not self.config):
            raise RuntimeError

    def init_library(self, bitflags=0):
        if (not dring.init(bitflags)):
            raise RuntimeError

        # register callbacks
        #cdef function[dring.CallbackWrapperBase] func;
        #ctypedef const map[string, SharedCallback] config_event_handlers
        #self.configuration_manager.registerConfHandlers(func)

    def start(self):
        if (not dring.start()):
            raise RuntimeError

    def stop(self):
        dring.fini()

    def poll_events(self):
        dring.pollEvents()

    def version(self):
        return dring.version().decode()

