#ifndef CALLBACK_CLIENT_H
#define CALLBACK_CLIENT_H

#include <functional>

#include <dring.h>
#include <configurationmanager_interface.h>

#include "callback_configurationmanager.h"

class CallbackClient {
    public:
        CallbackClient();
        ~CallbackClient();

        void registerEvents();
    
    private:
        std::unique_ptr<CallbackConfigurationManager> configurationManager;
};
#endif
