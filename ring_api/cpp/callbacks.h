#ifndef CALLBACKS_H
#define CALLBACKS_H

#include <functional>

#include <dring.h>
#include <configurationmanager_interface.h>

#include "logger.h" // is extra for devs

#include <Python.h>
#include "dring_cython.h" // has generated C callbacks

class Callbacks {
    public:
        Callbacks();
        ~Callbacks();

        void registerEvents();
};
#endif
