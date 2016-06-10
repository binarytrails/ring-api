from libc.stdint cimport *

from libcpp.string cimport string
from libcpp cimport bool as boolean
from libcpp.map cimport map as map
from libcpp.vector cimport vector

from ring_api.utils.std cimport *
from ring_api.interfaces.dring cimport *

cdef extern from "configurationmanager_interface.h" namespace "DRing":

    void registerConfHandlers(const map[
        string, shared_ptr[CallbackWrapperBase]] &)

    # account id != ring id
    vector[string] getAccountList()
    map[string, string] getAccountDetails(const string& accountID);

    # to: ring_id_dest, payloads: map[<mime-type>, <message>]
    uint64_t sendAccountTextMessage(const string& accountID, const string& to,
            const map[string, string]& payloads);


    ctypedef (const string&, const string&,
            const map[string, string]&) CbTypeIncomingAccountMessage

    cdef cppclass ConfigrationSignal:
        cppclass IncomingAccountMessage:
            const char* name # = "IncomingAccountMessage"
            # (account_id, from, payloads: map[<mime-type>, <message>]
            CbTypeIncomingAccountMessage cb_type

