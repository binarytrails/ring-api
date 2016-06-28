# cython: language_level=3
#
# Copyright (C) 2016 Savoir-faire Linux Inc
#
# Author: Seva Ivanov <seva.ivanov@savoirfairelinux.com>
# Author: Simon Zeni <simon.zeni@savoirfairelinux.com>
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301 USA.
#

# Keep the logic of the interfaces
# Apply the logical partitioning in the API layer

from libcpp.string cimport string
from libcpp.map cimport map as map

from ring_api.utils.std cimport *
from ring_api.utils.cython import *

from ring_api.interfaces cimport dring as dring_cpp
from ring_api.interfaces cimport configuration_manager as confman_cpp
from ring_api.interfaces cimport call_manager as callman_cpp
from ring_api.interfaces cimport video_manager as videoman_cpp
from ring_api.interfaces cimport cb_client as cb_client_cpp

global python_callbacks
python_callbacks = dict.fromkeys(['text_message'])

global python_callbacks_context

cdef public void incoming_account_message(
        const string& raw_account_id,
        const string& raw_from_ring_id,
        const map[string, string]& raw_content):

    account_id = bytes(raw_account_id).decode()
    from_ring_id = bytes(raw_from_ring_id).decode()

    content = dict()
    raw_content_dict = dict(raw_content)
    for raw_key in raw_content_dict:
        key = raw_key.decode()
        content[key] = raw_content_dict[raw_key].decode()

    global python_callbacks
    callback = python_callbacks['text_message']
    global python_callbacks_context
    context = python_callbacks_context

    if (callback):
        callback(context, str(account_id), str(from_ring_id), content)

cdef class CallbacksClient:
    cdef cb_client_cpp.CallbacksClient *_thisptr

    def __cinit__(self):
        self._thisptr = new cb_client_cpp.CallbacksClient()

    def __dealloc__(self):
        del self._thisptr

    def register_events(self):
        """Registers cython callback events"""

        self._thisptr.registerEvents()

cdef class ConfigurationManager:

    def account_details(self, account_id):
        """Gets account details

        Keyword argument:
        account_id -- account id string

        Return: account_details dict
        """
        cdef string raw_id = account_id.encode()

        return raw_dict_to_dict(confman_cpp.getAccountDetails(raw_id))

    def set_details(self, account_id, details):
        cdef string raw_id = account_id.encode()
        cdef map[string, string] raw_details

        for key in details:
            raw_details[key.encode()] = details[key].encode()

        confman_cpp.setAccountDetails(raw_id, raw_details)

    def set_account_active(self, account_id, active):
        """Set if this account can be used or not

        Keyword arguments:
        account_id   -- account id string
        active       -- status bool
        """
        confman_cpp.setAccountActive(account_id.encode(), active)

    def get_account_template(self, account_type):
        """Generate a template in function of the type.
        Type can be : SIP, IAX, IP2IP, RING

        Keyword argument:
        account_type -- account type string

        Return: template dict
        """
        raw_template = confman_cpp.getAccountTemplate(account_type.encode())

        return raw_dict_to_dict(raw_template)

    def add_account(self, details):
        """Add a new account to the daemon

        Keyword argument:
        details -- account details map[string, string]

        Return: account_id string
        """
        cdef map[string, string] raw_details

        for key in details:
            raw_details[key.encode()] = details[key].encode()

        cdef string raw_account_id = confman_cpp.addAccount(raw_details)

        return raw_account_id.decode()

    def remove_account(self, account_id):
        """Remove an account from the daemon

        Keywork argument:
        account_id -- account id string
        """
        confman_cpp.removeAccount(account_id.encode())

    def accounts(self):
        """List user accounts (not ring ids)

        Return: accounts list
        """
        return raw_list_to_list(confman_cpp.getAccountList())

    def send_text_message(self, account_id, ring_id, content):
        """Sends a text message

        Keyword arguments:
        account_id  -- account id string
        ring_id     -- ring id destination string
        content     -- dict of content defined as {<mime-type>: <message>}

        No return
        """
        cdef string raw_account_id = account_id.encode()
        cdef string raw_ring_id = ring_id.encode()
        cdef map[string, string] raw_content

        for key, value in content.iteritems():
            raw_content[key.encode()] = value.encode()

        confman_cpp.sendAccountTextMessage(
                raw_account_id, raw_ring_id, raw_content)

    def validate_certificate(self, account_id, certificate):
        """A key-value list of all certificate validation

        Keyword arguments:
        account_id  -- account id string
        certificate -- certificate string

        Return: valid certificate list
        """
        raw_valid_certif = confman_cpp.validateCertificate(account_id.encode(), certificate.encode())

        return raw_dict_to_dict(raw_valid_certif)

    def get_certificate_details(self, certificate):
        """A key-value list of all certificate details

        Keyword argument:
        certificate -- certificate string

        Return: certificate details dict
        """
        return raw_dict_to_dict(confman_cpp.getCertificateDetails(certificate.encode()))

    def get_pinned_certificates(self):
        """A list of all known certificate IDs

        Return: pinned certificates list
        """
        return raw_list_to_list(confman_cpp.getPinnedCertificates())

    def pin_certificate(self, certificate, local):
        """True to save the certificate in the daemon local store

        Keyword arguments:
        certificate -- raw certificate int list
        local       -- true to save bool

        Return: IDs of the pinned certificate list
        """
        return raw_list_to_list(confman_cpp.pinCertificate(certificate, local))

    def unpin_certificate(self, cert_id):
        """Unpin a certificate

        Keyword arguments:
        cert_id     -- certificate id string

        Return: True if unpinned bool
        """
        return confman_cpp.unpinCertificate(cert_id.encode())

    def pin_remote_certificate(account_id, cert_id):
        """Pin a certificate to an account

        Keyword arguments:
        account_id  -- account id string
        cert_id     -- certificate id string

        Return: success bool
        """
        return confman_cpp.pinRemoteCertificate(account_id.encode(), cert_id.encode())

    def set_certificate_status(account_id, cert_id, status):
        """Set a status if an account certificate

        Keyword arguments:
        account_id  -- account id string
        cert_id     -- certificate id string
        status      -- 'UNDEFINED', 'ALLOWED' or 'BANNED' string

        Return: True if the state is set bool
        """
        return confman_cpp.setCertificateStatus(account_id.encode(),
            cert_id.encode(),
            status.encode())

cdef class VideoManager:
    def devices(self):
        """List the available video devices

        Return: devices list
        """
        return raw_list_to_list(videoman_cpp.getDeviceList())
    
    def get_settings(self, name):
        """Settings of a given device

        Keyword arguments:
        name      -- device id string

        Return: settings dict
        """
        return raw_dict_to_dict(videoman_cpp.getSettings(name.encode()))
    
    def apply_settings(self, name, settings):
        """Change the settings of a given device

        Keyword arguments:
        name      -- device id string
        settings  -- settings dict
        """
        cdef map[string, string] raw_settings

        for key, value in settings.iteritems():
            raw_settings[key.encode()] = value.encode()

        videoman_cpp.applySettings(name.encode(), raw_settings)

    def set_default_device(self, dev):  
        videoman_cpp.setDefaultDevice(dev.encode())
    
    def get_default_device(self):
        return videoman_cpp.getDefaultDevice().decode()

    def start_camera(self):
        videoman_cpp.startCamera()

    def stop_camera(self):
        videoman_cpp.stopCamera()
    
    def switch_input(self, resource):
        return videoman_cpp.switchInput(resource.encode())

    def has_camera_started(self):
        return videoman_cpp.hasCameraStarted()

cdef class CallManager:

    def place_call(self, account_id, to):
        """Place a new call between two users

        Keyword argument:
        account_id  -- account string
        to          -- ring_id string

        Return: call_id string
        """

        raw_call_id = callman_cpp.placeCall(account_id.encode(), to.encode());

        return raw_call_id.decode()

    def refuse(self, call_id):
        """Refuse an incoming call

        Keyword argument:
        call_id -- call id string

        Return: status bool
        """
        return callman_cpp.refuse(call_id.encode());

    def accept(self, call_id):
        """Accept an incoming call

        Keyword argument:
        call_id -- call id string

        Return: status bool
        """
        return callman_cpp.accept(call_id.encode());

    def hang_up(self, call_id):
        """Hang up a call in state 'CURRENT' or 'HOLD'

        Keyword argument:
        call_id -- call id string

        Return: status bool
        """
        return callman_cpp.hangUp(call_id.encode());

    def hold(self, call_id):
        """Place a call in state 'HOLD'

        Keyword argument:
        call_id -- call id string

        Return: status bool
        """
        return callman_cpp.hold(call_id.encode());

    def unhold(self, call_id):
        """Take a call off 'HOLD', and place it in state 'CURRENT'

        Keyword argument:
        call_id -- call id string

        Return: status bool
        """
        return callman_cpp.unhold(call_id.encode());


cdef class PresenceManager:
    pass

cdef class Dring:
    cdef:
        readonly int _FLAG_DEBUG
        readonly int _FLAG_CONSOLE_LOG
        readonly int _FLAG_AUTOANSWER

    cdef public ConfigurationManager config
    cdef public VideoManager video
    cdef public CallManager call
    cdef public PresenceManager pres
    cdef CallbacksClient cb_client

    def __cinit__(self):
        self._FLAG_DEBUG          = dring_cpp.DRING_FLAG_DEBUG
        self._FLAG_CONSOLE_LOG    = dring_cpp.DRING_FLAG_CONSOLE_LOG
        self._FLAG_AUTOANSWER     = dring_cpp.DRING_FLAG_AUTOANSWER

        self.config = ConfigurationManager()
        if (not self.config):
            raise RuntimeError

        self.video = VideoManager()
        if (not self.video):
            raise RuntimeError

        self.call = CallManager()
        if (not self.video):
            raise RuntimeError

        self.pres = PresenceManager()
        if (not self.video):
            raise RuntimeError

    def init_library(self, bitflags=0):

        if (not dring_cpp.init(bitflags)):
            raise RuntimeError

        self.cb_client = CallbacksClient()
        self.cb_client.register_events()

    def start(self):
        if (not dring_cpp.start()):
            raise RuntimeError

    def stop(self):
        dring_cpp.fini()

    def poll_events(self):
        dring_cpp.pollEvents()

    def version(self):
        return dring_cpp.version().decode()

    def callbacks_to_register(self):
        """Returns the python callbacks that will be triggered dring signals.
        The signals are the dict keys.
        """
        global python_callbacks
        return python_callbacks

    def register_callbacks(self, callbacks, context):
        """Registers the python callbacks received as dict values.
        The corresponding signals are defined as keys.
        Expects the dict with keys defined by the callbacks() method.

        No return
        """
        global python_callbacks
        try:
            for key, value in python_callbacks.items():
                python_callbacks[key] = callbacks[key]
        except KeyError as e:
            raise KeyError("KeyError: %s. You can't change the keys." % e)

        global python_callbacks_context
        python_callbacks_context = context
