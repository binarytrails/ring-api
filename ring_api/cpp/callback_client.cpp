#include "callback_client.h"

CallbackClient::CallbackClient()
{
    configurationManager.reset(new CallbackConfigurationManager {});
}

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

    auto confM = configurationManager.get();

    const std::map<std::string, SharedCallback> configEvHandlers = {
        exportable_callback<ConfigurationSignal::IncomingAccountMessage>(
            bind(&CallbackConfigurationManager::incomingAccountMessage,
                confM, _1, _2, _3 ))
    };

    registerConfHandlers(configEvHandlers);
}
