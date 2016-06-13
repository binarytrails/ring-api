#include "callback_configurationmanager.h"

CallbackConfigurationManager::CallbackConfigurationManager(){}

void CallbackConfigurationManager::incomingAccountMessage(const std::string& accountID,
    const std::string& from,
    const std::map<std::string, std::string>& payloads)
{   
    RING_INFO("Account Id : %s", accountID.c_str());
    RING_INFO("From : %s", from.c_str());
    RING_INFO("Payloads: ");
    for(auto& it : payloads)
        RING_INFO("%s : %s", it.first.c_str(), it.second.c_str());
}

