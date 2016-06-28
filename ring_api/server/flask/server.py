from flask import Flask
from flask_restful import Api

from flask_socketio import SocketIO

from ring_api.server.flask import socketio_cb_api as cb_api
from ring_api.server.flask.api import account, video, call

class FlaskServer:
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
        self._register_callbacks()

    def _add_resources(self):
        # Configuration manager related resources
        self.api.add_resource(account.Accounts, '/accounts/',
            resource_class_kwargs={'dring': self.dring})
        
        self.api.add_resource(account.AccountsDetails,
            '/accounts/<account_id>/details/',
            resource_class_kwargs={'dring': self.dring})
        
        # Video manager related resources
        self.api.add_resource(video.Devices,
            '/settings/video/devices/',
            resource_class_kwargs={'dring': self.dring})

        self.api.add_resource(video.Settings,
            '/settings/video/settings/<device_name>/',
            resource_class_kwargs={'dring': self.dring})

        self.api.add_resource(video.Default,
            '/settings/video/devices/default/',
            resource_class_kwargs={'dring': self.dring})

        self.api.add_resource(video.Start,
            '/settings/video/camera/start/',
            resource_class_kwargs={'dring': self.dring})

        self.api.add_resource(video.Stop,
            '/settings/video/camera/stop/',
            resource_class_kwargs={'dring': self.dring})

        self.api.add_resource(video.Switch,
            '/settings/video/camera/switch/',
            resource_class_kwargs={'dring': self.dring})

        self.api.add_resource(video.Status,
            '/settings/video/camera/status/',
            resource_class_kwargs={'dring': self.dring})

        # Call manager related resources
        self.api.add_resource(call.Call,
            '/call/place/<account_id>/<to>/',
            resource_class_kwargs={'dring': self.dring})

        self.api.add_resource(call.Refuse,
            '/call/refuse/<call_id>',
            resource_class_kwargs={'dring': self.dring})

        self.api.add_resource(call.Accept,
            '/call/accept/<call_id>',
            resource_class_kwargs={'dring': self.dring})

        self.api.add_resource(call.HangUp,
            '/call/hang_up/<call_id>',
            resource_class_kwargs={'dring': self.dring})

        self.api.add_resource(call.Hold,
            '/call/hold/<call_id>',
            resource_class_kwargs={'dring': self.dring})

        self.api.add_resource(call.Unhold,
            '/call/unhold/<call_id>',
            resource_class_kwargs={'dring': self.dring})

    def _register_callbacks(self):
        callbacks = self.dring.callbacks_to_register()

        # TODO add dynamically from implemented function names
        callbacks['text_message'] = cb_api.text_message

        self.dring.register_callbacks(callbacks, context=self.socketio)

    def start(self):
        self.socketio.run(self.app, host=self.host, port=self.port)

    def stop(self):
        pass

