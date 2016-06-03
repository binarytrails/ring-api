from libcpp cimport bool as boolean

cdef extern from "<memory>" namespace "std" nogil:
    cdef cppclass shared_ptr[T]:
        shared_ptr() except +
        T* get()
        T operator*()
        void reset(T*)

cdef extern from "<future>" namespace "std" nogil:
    cdef cppclass shared_future[T]:
        shared_future() except +
        boolean valid() const

    cdef cppclass future[T]:
        future() except +
        boolean valid() const
        shared_future[T] share()

cdef extern from "<functional>" namespace "std" nogil:
    cdef cppclass function[T]:
        function() except +
        function(const T&)

