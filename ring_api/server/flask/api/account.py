from flask import jsonify, request, abort
from flask_restful import Resource
from flask_socketio import SocketIO

class Accounts(Resource):
    def __init__(self, dring, socketio):
        self.dring = dring
        self.socketio = socketio

    def get(self):
        return jsonify({'accounts': self.dring.config.accounts()})

class AccountsDetails(Resource):
    def __init__(self, dring, socketio):
        self.dring = dring
        self.socketio = socketio

    def get(self, account_id):
        data = request.args
        if (not data):
            abort(404)
        elif ('type' not in data):
            return abort(404)
        
        account_type = data.get('type')

        if (account_type == 'default'):
            details = self.dring.config.account_details(account_id)
            return jsonify(details)
        elif (account_type == 'volatile'):
            pass

        return abort(404)

