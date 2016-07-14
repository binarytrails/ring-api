#
# Copyright (C) 2016 Savoir-faire Linux Inc
#
# Authors:  Seva Ivanov <seva.ivanov@savoirfairelinux.com>
#           Simon Zeni  <simon.zeni@savoirfairelinux.com>
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

from flask import Flask
from flask_restful import Api

import threading
import asyncio
import websockets
from websockets import exceptions as ws_ex

from ring_api.server.flask.cb_api import websockets as cb_api
from ring_api.server.flask.api import (
    account, video, messages, calls, certificate, audio, crypto, codec)

class FlaskServer:

    websockets = list()
    ws_messages = asyncio.Queue()

    def __init__(self, host, port, dring, dring_pollevents_interval, verbose):
        self.host = host
        self.port = port
        self.dring = dring
        self.dring_pollevents_interval = dring_pollevents_interval
        self.verbose = verbose

        self.app = Flask(__name__)
        self.app.config['SECRET_KEY'] = 't0p_s3cr3t'
        self.app.config.update(
            PROPAGATE_EXCEPTIONS = True
        )

        self.api = Api(self.app, catch_all_404s=True)
        self._init_api_resources()

        self._init_websockets()
        self._register_callbacks()

    def _init_api_resources(self):
        """Initializes the Flask-REST API resources

        Keep the same order as in the rest-api.json.
        """

        # Accounts
        self.api.add_resource(account.Account, '/account/',
            resource_class_kwargs={'dring': self.dring})

        self.api.add_resource(account.Accounts, '/accounts/',
            resource_class_kwargs={'dring': self.dring})

        self.api.add_resource(account.AccountsID, '/accounts/<account_id>/',
            resource_class_kwargs={'dring': self.dring})

        self.api.add_resource(account.AccountsDetails,
            '/accounts/<account_id>/details/',
            resource_class_kwargs={'dring': self.dring})

        self.api.add_resource(account.AccountsCodecs,
            '/accounts/<account_id>/codecs/',
            '/accounts/<account_id>/codecs/<codec_id>/',
            resource_class_kwargs={'dring': self.dring})

        self.api.add_resource(account.AccountsCall,
            '/accounts/<account_id>/call/',
            resource_class_kwargs={'dring': self.dring})

        self.api.add_resource(account.AccountsCertificates,
            '/accounts/<account_id>/certificates/<cert_id>/',
            resource_class_kwargs={'dring': self.dring})

        self.api.add_resource(account.AccountsMessage,
            '/accounts/<account_id>/message/',
            resource_class_kwargs={'dring': self.dring})

        # Messages
        self.api.add_resource(messages.Messages,
            '/messages/<message_id>/',
            resource_class_kwargs={'dring': self.dring})

        # Calls
        self.api.add_resource(calls.Calls,
            '/calls/<call_id>/',
            resource_class_kwargs={'dring': self.dring})

        # Codecs
        self.api.add_resource(codec.Codecs,
            '/codecs/',
            resource_class_kwargs={'dring': self.dring})

        # Crypto
        self.api.add_resource(crypto.Tls,
            '/crypto/tls/',
            resource_class_kwargs={'dring': self.dring})


        # Certificate
        self.api.add_resource(certificate.Certificate,
            '/certificates/',
            resource_class_kwargs={'dring': self.dring})

        self.api.add_resource(certificate.Certificates,
            '/certificate/<cert_id>/',
            resource_class_kwargs={'dring': self.dring})

        # Audio
        self.api.add_resource(audio.Plugins,
            '/audio/plugins/',
            resource_class_kwargs={'dring': self.dring})

        # Video
        self.api.add_resource(video.VideoDevices,
            '/video/devices/',
            resource_class_kwargs={'dring': self.dring})

        self.api.add_resource(video.VideoSettings,
            '/video/<device_id>/settings/',
            resource_class_kwargs={'dring': self.dring})

        self.api.add_resource(video.VideoCamera,
            '/video/camera/',
            resource_class_kwargs={'dring': self.dring})

    def _init_websockets(self):
        self.ws_eventloop = asyncio.new_event_loop()
        asyncio.set_event_loop(self.ws_eventloop)

        # TODO handle if closed and set as class var for rest api to inform
        self.ws_server = websockets.serve(self.ws_handle, '127.0.0.1', 5678)

        self.ws_eventloop.create_task(self.ws_server)
        self.ws_eventloop.create_task(self.ws_notify())

    def _register_callbacks(self):
        """ Registers Ring-daemon callbacks """
        callbacks = self.dring.callbacks_to_register()

        # TODO add dynamically from implemented function names
        callbacks['account_message'] = cb_api.account_message

        ws_context = {
            'eventloop': self.ws_eventloop,
            'queue': self.ws_messages}

        self.dring.register_callbacks(callbacks, context=ws_context)

    def run_websockets(self):
        """ Starts the asyncio eventloop for the websockets

        It needs to be run as main process @TODO
        """
        self.ws_eventloop.run_forever()

    def run_rest(self):
        """ Starts the RESTful Flask application

        No return
        """
        # use_reloader is set to False because if it's set to True
        # it expects to run in the main thread

        self.app.run(host=self.host, port=self.port,
                debug=True, use_reloader=False)

    def stop(self):
        """ TODO """
        pass

    # WebSockets using AsyncIO

    async def ws_handle(self, websocket, path):
        """ Task handle which is run for every websocket connection.

        Keyword arguments:
        websocket   --    websocket instance using asyncio library
        path        --    websocket namespace

        No return
        """
        if (websocket not in self.websockets):
            self.websockets.append(websocket)

            if (self.verbose):
                print('server: adding new socket: %s' % str(websocket))

        while True:
            # Keeps the websocket alive by the current design
            # see: https://github.com/aaugustin/websockets/issues/122
            await asyncio.sleep(60)

            if (websocket not in self.websockets):
                if (self.verbose):
                    print('server: closing websocket %s' % websocket)
                break

    async def ws_notify(self):
        """ Task notify which listens for new callback messages and send them
        to all connected websockets.

        'Dirty hack' issue:
        Asyncio Queue class is not thread safe.

        It means that in the cb_api/websockets.py, we have to use the call
        queue.put_nowait() in call_soon_threadsafe() where queue is ws_messages.
        This means that the await on ws_messages.get() will never happen here.

        In case, we wish to use the asyncio concurrency, we will need to use:
        'eventloop.create_task(queue.put(message))' in cb_api/websockets.py.
        However, since the Asyncio Queue is not thread safe, it won't work.

        The latter brings this 'dirty hack' where I use the asyncio websockets
        implementation but *instead of awaiting messages, we refresh every 'n'
        seconds* with a combination of queue.get_nowait().

        The refresh is based on the dring poll_events() interval.

        A clean solution would be to find a Queue library supporting both.
        """

        if (self.verbose):
            print('server: waiting for websockets notifications')

        while True:
            # --------------FIXME dirty hack:------------------
            await asyncio.sleep(self.dring_pollevents_interval)

            for i in range(0, self.ws_messages.qsize()):
                # should be in a loop to get them all
                try:
                    message = self.ws_messages.get_nowait()
                except asyncio.queues.QueueEmpty:
                    break

            # Should be only the below line without the previous for loop:
            #message = await self.ws_messages.get()
            # -------------------------------------------------

                if (self.verbose):
                    print('server: got "%s"' % message)

                for websocket in self.websockets:

                    if (self.verbose):
                        print('server: sending "%s" to %s' % (message, websocket))

                    try:
                        await websocket.send(message)

                    except ws_ex.ConnectionClosed:
                        self.websockets.remove(websocket)
                        if (self.verbose):
                            print('server: connection closed to %s' % websocket)

