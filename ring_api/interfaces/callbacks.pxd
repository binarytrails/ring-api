
cdef extern from "callbacks.h":

    cdef cppclass Callbacks:
        Callbacks() except +
        void registerEvents()

