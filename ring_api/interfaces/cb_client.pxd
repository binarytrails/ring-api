
cdef extern from "cb_client.h":

    cdef cppclass CallbacksClient:
        CallbacksClient() except +
        void registerEvents()

