# cython: language_level=3

# Keep the logic of the interfaces
# Apply the logical partitioning in the API layer

from libcpp.string cimport string
from libcpp.map cimport map as map

from ring_api.utils.std cimport *
from ring_api.interfaces cimport dring as dring_cpp
from ring_api.interfaces cimport configuration_manager as confman_cpp
from ring_api.interfaces cimport callbacks as callbacks_cpp

global python_callbacks # TODO

cdef public void incoming_account_message(const string& account_id,
        const string& from_ring_id, const map[string, string]& payloads):
    print('-------------------incoming_account_message in cython------------------------')

cdef class Callbacks:
    cdef callbacks_cpp.Callbacks *_thisptr

    def __cinit__(self):
        self._thisptr = new callbacks_cpp.Callbacks()

    def __dealloc__(self):
        del self._thisptr

    def register_events(self):
        """@TODO"""

        self._thisptr.registerEvents()

cdef class ConfigurationManager:

    def accounts(self):
        """List user accounts (not ring ids)

        Return: accounts list
        """
        accounts = list()
        raw_accounts = confman_cpp.getAccountList()

        for i, account in enumerate(raw_accounts):
            accounts.append(account.decode())

        return accounts

    def account_details(self, account_id):
        """Gets account details

        Keyword arguments:
        account_id -- account id string

        Return: account details dict
        """
        cdef string raw_id = account_id.encode()
        details = dict()
        raw_dict = confman_cpp.getAccountDetails(raw_id)

        for key, value in raw_dict.iteritems():
            details[key.decode()] = value.decode()

        return details

    def send_text_message(self, account_id, ring_id, content_map):
        """Sends a text message

        Keyword arguments:
        account_id  -- account id string
        ring_id     -- ring id destination string
        content_map -- map of content defined as [<mime-type>, <message>]

        No return
        """
        cdef string raw_account_id = account_id.encode()
        cdef string raw_ring_id = ring_id.encode()
        cdef map[string, string] raw_content_map

        for key, value in content_map.iteritems():
            raw_content_map[key.encode()] = value.encode()

        confman_cpp.sendAccountTextMessage(
                raw_account_id, raw_ring_id, raw_content_map)

cdef class Dring:
    cdef:
        readonly int _FLAG_DEBUG
        readonly int _FLAG_CONSOLE_LOG
        readonly int _FLAG_AUTOANSWER

    cdef public ConfigurationManager config
    # TODO keep public?
    cdef public Callbacks callbacks

    def __cinit__(self):
        self._FLAG_DEBUG          = dring_cpp.DRING_FLAG_DEBUG
        self._FLAG_CONSOLE_LOG    = dring_cpp.DRING_FLAG_CONSOLE_LOG
        self._FLAG_AUTOANSWER     = dring_cpp.DRING_FLAG_AUTOANSWER

        self.config = ConfigurationManager()
        if (not self.config):
            raise RuntimeError

    def init_library(self, bitflags=0):

        if (not dring_cpp.init(bitflags)):
            raise RuntimeError

        self.callbacks = Callbacks()
        self.callbacks.register_events()

    def start(self):
        if (not dring_cpp.start()):
            raise RuntimeError

    def stop(self):
        dring_cpp.fini()

    def poll_events(self):
        dring_cpp.pollEvents()

    def version(self):
        return dring_cpp.version().decode()

