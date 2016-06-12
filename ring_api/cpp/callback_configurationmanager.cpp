#include "callback_configurationmanager.h"

CallbackConfigurationManager::CallbackConfigurationManager(){}

void incomingAccountMessage(const std::string& accountID,
    const std::string& from,
    const std::map<std::string, std::string>& payloads)
{   
    RING_INFO("SLIPPING JIMMY RECIEVED A MESSAGE!");
}

