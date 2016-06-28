from flask import jsonify, request, abort
from flask import copy_current_request_context
from flask_restful import Resource
from flask_socketio import SocketIO

class Accounts(Resource):
    def __init__(self, dring):
        self.dring = dring

    def get(self):
        return jsonify({'accounts': self.dring.config.accounts()})

class AccountsDetails(Resource):
    def __init__(self, dring):
        self.dring = dring

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

# socketio callbacks

def text_message(socketio, account_id, from_ring_id, content):
    """Receives a text message

    Keyword arguments:
    socketio        -- context as instance to emit to websockets
    account_id      -- account id string
    from_ring_id    -- ring id string
    content         -- dict of content defined as [<mime-type>, <message>]
    """
    print(id(socketio))
    socketio.emit('text_message', {
        'account_id': account_id,
        'from_ring_id': from_ring_id,
        'content': content
    })

