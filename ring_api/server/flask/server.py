from flask import Flask, request
from flask_restful import Api

from flask_socketio import SocketIO

from ring_api.server.flask import socketio_cb_api as cb_api
from ring_api.server.flask.api import account

global io
global dring

class FlaskServer:
    clients = []

    def __init__(self, host, port, _dring):
        self.host = host
        self.port = port
        self.dring = _dring

        self.app = Flask(__name__)
        self.app.config['SECRET_KEY'] = 't0p_s3cr3t'
        self.app.config.update(
            PROPAGATE_EXCEPTIONS = True
        )
        self.api = Api(self.app, catch_all_404s=True)

        self.socketio = SocketIO(self.app)
        self.socketio.on('connect')(connect)
        self.socketio.on('disconnect')(disconnect)
        self.socketio.on('emit_test')(emit_test)

        global io
        io = self.socketio
        global dring
        dring = self.dring

        self._add_resources()
        self._register_callbacks()

    def _add_resources(self):
        """Keep the same order as in the rest-api.json."""

        # Accounts
        self.api.add_resource(account.Accounts, '/accounts/',
            resource_class_kwargs={'dring': self.dring})

        self.api.add_resource(account.AccountsDetails,
            '/accounts/<account_id>/details/',
            resource_class_kwargs={'dring': self.dring})

        # Codecs
        # Crypto
        # Video
        # Audio
        # Video

    def _register_callbacks(self):
        callbacks = self.dring.callbacks_to_register()

        # TODO add dynamically from implemented function names
        callbacks['text_message'] = cb_api.text_message

        self.dring.register_callbacks(callbacks)
        self.dring.update_callbacks_context(self.socketio)

    def start(self):
        self.socketio.run(self.app, host=self.host, port=self.port)


    def stop(self):
        pass

def connect():
    global dring
    global io
    dring.update_callbacks_context(io)
    print('New client %s connected' % request.namespace)
    #clients.append(request.namespace)

def disconnect():
    print('New client %s disconnected' % request.namespace)
    #clients.remove(request.namespace)

def emit_test():
    io.emit('text_message', {'data': 'helloppppp'})

