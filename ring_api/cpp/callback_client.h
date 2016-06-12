#ifndef CALLBACK_CLIENT_H
#define CALLBACK_CLIENT_H

#include <cstdlib>
#include <iostream>
#include <cstring>
#include <stdexcept>

#include <memory>
#include <functional>

#include <dring.h>
#include <configurationmanager_interface.h>

#include "logger.h" // TODO remove

#include "callback_configurationmanager.h"

class CallbackConfigurationManager;

class CallbackClient {
    public:
        CallbackClient();
        ~CallbackClient();

        void registerEvents();
    
    private:
        std::unique_ptr<CallbackConfigurationManager> configurationManager;
};
#endif
