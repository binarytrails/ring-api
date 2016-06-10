from libcpp.string cimport string
from libcpp cimport bool as boolean
from libcpp.utility cimport pair

from ring_api.utils.std cimport *

cdef extern from "dring.h" namespace "DRing":

    #ctypedef pair[string, shared_ptr[CallbackWrapperBase]] ExportableCallbackType
    #ctypedef shared_ptr[CallbackWrapperBase] SharedCallbackType

    cdef enum InitFlag:
        DRING_FLAG_DEBUG       = 1<<0
        DRING_FLAG_CONSOLE_LOG = 1<<1
        DRING_FLAG_AUTOANSWER  = 1<<2

    const char* version()
    boolean init(InitFlag flags)
    boolean start(const string& config_file)
    boolean start()
    void fini()
    void pollEvents()

    cdef cppclass CallbackWrapperBase:
        CallbackWrapperBase() except +

    cdef cppclass CallbackWrapper[T](CallbackWrapperBase):
        CallbackWrapper() except +
        CallbackWrapper(function[T]&& func)
        CallbackWrapper(shared_ptr[T] p)

        const T& operator*()
        #const T operator boolean()

    # TODO reference in type type
    #pair[string, shared_ptr[CallbackWrapperBase]] exportable_callback(
    #        function[T.cb_type] func)

