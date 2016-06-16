#ifndef CB_CLIENT_H
#define CB_CLIENT_H

#include <functional>

#include <dring.h>
#include <configurationmanager_interface.h>

#include "logger.h" // is extra for devs

#include <Python.h>
#include "dring_cython.h" // has generated C callbacks

class CallbacksClient {
    public:
        CallbacksClient();
        ~CallbacksClient();

        void registerEvents();
};
#endif
