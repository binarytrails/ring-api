
cdef extern from "<memory>" namespace "std" nogil:
    cdef cppclass shared_ptr[T]:
        shared_ptr() except +
        T* get()
        T operator*()
        void reset(T*)

