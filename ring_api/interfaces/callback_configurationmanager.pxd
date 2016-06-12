from libcpp.string cimport string
from libcpp cimport bool as boolean
from libcpp.utility cimport pair
from libcpp.map cimport map as map

from ring_api.utils.std cimport *

cdef extern from "callback_configurationmanager.h":

    cdef cppclass CallbackConfigurationManager:
        CallbackConfigurationManager() except +
        
        # Callbacks
        void incomingAccountMessage(const string& accountID,
            const string& from_ring_id,
            const map[string, string]& payloads)

