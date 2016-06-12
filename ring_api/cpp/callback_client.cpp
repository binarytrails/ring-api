#include "callback_client.h"

CallbackClient::CallbackClient(){}

CallbackClient::~CallbackClient()
{
    configurationManager.reset();
}

void CallbackClient::registerEvents()
{
    // Must be performed after Dring::init() method
    
    using namespace std::placeholders;

    using std::bind;
    using DRing::exportable_callback;
    using DRing::ConfigurationSignal;

    using SharedCallback = std::shared_ptr<DRing::CallbackWrapperBase>;

    //auto confM = configurationManager.get();

    const std::map<std::string, SharedCallback> configEvHandlers = {
        exportable_callback<ConfigurationSignal::IncomingAccountMessage>(
            //bind(&CallbackConfigurationManager::incomingAccountMessage,
            //confM, _1, _2, _3 ))
            [] (const std::string& accountID, const std::string& from,
                const std::map<std::string, std::string>& payloads)
            {
                RING_INFO("accountID : %s", accountID.c_str());
                RING_INFO("from : %s", from.c_str());
                RING_INFO("payloads");
                for(auto& it : payloads)
                    RING_INFO("%s : %s", it.first.c_str(),
                            it.second.c_str());
            })
    };

    registerConfHandlers(configEvHandlers);
}
