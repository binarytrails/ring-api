from flask import Flask
from flask_restful import Api
from flask_socketio import SocketIO # TODO remove

import threading
import asyncio
import websockets
from websockets import exceptions as ws_ex

from ring_api.server.flask.cb_api import websockets as cb_api
from ring_api.server.flask.api import account, video, calls, certificate

class FlaskServer:

    websockets = list()
    ws_messages = asyncio.Queue()

    def __init__(self, host, port, dring):
        self.host = host
        self.port = port
        self.dring = dring

        self.app = Flask(__name__)
        self.app.config['SECRET_KEY'] = 't0p_s3cr3t'
        self.app.config.update(
            PROPAGATE_EXCEPTIONS = True
        )
        self.api = Api(self.app, catch_all_404s=True)
        self.socketio = SocketIO(self.app)

        self._add_resources()

    def _add_resources(self):
        """Keep the same order as in the rest-api.json."""

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

        self.api.add_resource(account.AccountsCall,
            '/accounts/<account_id>/call/',
            resource_class_kwargs={'dring': self.dring})

        self.api.add_resource(account.AccountsCertificates,
            '/accounts/<account_id>/certificates/<cert_id>/',
            resource_class_kwargs={'dring': self.dring})

        # Calls

        self.api.add_resource(calls.Calls,
            '/calls/<call_id>/',
            resource_class_kwargs={'dring': self.dring})

        # Codecs
        # Crypto
        # Certificate

        self.api.add_resource(certificate.Certificate,
            '/certificates/',
            resource_class_kwargs={'dring': self.dring})

        self.api.add_resource(certificate.Certificates,
            '/certificate/<cert_id>/',
            resource_class_kwargs={'dring': self.dring})

        # Audio
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

    def _register_callbacks(self):
        callbacks = self.dring.callbacks_to_register()

        # TODO add dynamically from implemented function names
        callbacks['text_message'] = cb_api.text_message

        self.dring.register_callbacks(callbacks, context=self)

    async def ws_handle(self, websocket, path):
        if (websocket not in self.websockets):
            self.websockets.append(websocket)
            print('server: adding new socket: %s' % str(websocket))

        print('server: sending "welcome" to %s' % str(websocket))
        await websocket.send('welcome')

        while True:
            # keeps the websocket alive by the current design
            # see: https://github.com/aaugustin/websockets/issues/122
            await asyncio.sleep(60)
            if (websocket not in self.websockets):
                print('server: closing websocket %s' % websocket)
                break

    async def ws_notify(self):
        while True:
            message = await self.ws_messages.get()
            print('server: got "%s"' % message)

            for websocket in self.websockets:
                print('server: sending "%s" to %s' % (message, websocket))
                try:
                    await websocket.send(message)
                except ws_ex.ConnectionClosed:
                    self.websockets.remove(websocket)
                    print('server: connection closed to %s' % websocket)

    def start_ws_eventloop(self):
        self.ws_eventloop = asyncio.new_event_loop()
        asyncio.set_event_loop(self.ws_eventloop)

        # TODO register
        self.ws_server = websockets.serve(
                self.ws_handle, '127.0.0.1', 5678)

        self.ws_eventloop.create_task(self.ws_server)
        self.ws_eventloop.create_task(self.ws_notify())

        self.ws_eventloop.run_forever()

    def start(self):
        self.ws_eventloop_thread = threading.Thread(
                target=self.start_ws_eventloop)
        self.ws_eventloop_thread.start()

        self._register_callbacks()

        # blocking call; TODO remove socketio
        self.socketio.run(self.app, host=self.host, port=self.port)

    def stop(self):
        # TODO
        pass

