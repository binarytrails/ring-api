
cdef extern from "callback_client.h":

    cdef cppclass CallbackClient:
        CallbackClient() except +
        void registerEvents()

