from libcpp.string cimport string
from libcpp cimport bool as boolean

cdef extern from "dring.h" namespace "DRing":
    cdef enum InitFlag:
        DRING_FLAG_DEBUG       = 1<<0
        DRING_FLAG_CONSOLE_LOG = 1<<1
        DRING_FLAG_AUTOANSWER  = 1<<2

    boolean init(InitFlag flags)

    boolean start(const string& config_file)
    boolean start()

    const char* version();

    #cdef cppclass CallbackWrapperBase:

