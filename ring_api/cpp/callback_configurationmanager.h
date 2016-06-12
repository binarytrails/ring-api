#ifndef CALLBACK_CONFIGURATIONMANAGER_H
#define CALLBACK_CONFIGURATIONMANAGER_H

#include "configurationmanager_interface.h"

#include "logger.h" // TODO only for dev stage; remove.

class CallbackConfigurationManager
{
    public:
        CallbackConfigurationManager();

        void incomingAccountMessage(const std::string& accountID,
            const std::string& from,
            const std::map<std::string, std::string>& payloads);
};
#endif
