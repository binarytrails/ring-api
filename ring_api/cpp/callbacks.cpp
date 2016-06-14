#include "callbacks.h"

Callbacks::Callbacks(){}

Callbacks::~Callbacks(){}

void Callbacks::registerEvents()
{
    /* Must be executed after Dring::init() method.
     * Binding after Cython methods from the generated C header.
     */
    
    using namespace std::placeholders;

    using std::bind;
    using DRing::exportable_callback;
    using DRing::ConfigurationSignal;

    using SharedCallback = std::shared_ptr<DRing::CallbackWrapperBase>;

    const std::map<std::string, SharedCallback> configEvHandlers = {
        exportable_callback<ConfigurationSignal::IncomingAccountMessage>(
            bind(&incoming_account_message, _1, _2, _3))
    };

    registerConfHandlers(configEvHandlers);
}
