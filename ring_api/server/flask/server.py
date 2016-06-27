from flask import Flask
from flask_restful import Api
from flask_socketio import SocketIO

from ring_api.server.flask.api import account

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

    def _add_resources(self):
        self.api.add_resource(account.Accounts, '/accounts/',
            resource_class_kwargs={
                'dring': self.dring,
                'socketio': self.socketio})
        
        self.api.add_resource(account.AccountsDetails,
            '/accounts/<account_id>/details/',
            resource_class_kwargs={
                'dring': self.dring,
                'socketio': self.socketio})

    def start(self):
        self.socketio.run(self.app, host=self.host, port=self.port)

    def stop(self):
        pass

