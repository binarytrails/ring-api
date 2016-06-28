from flask import jsonify, request, abort
from flask_restful import Resource
from flask_socketio import SocketIO

class Call(Resource):
    def __init__(self, dring):
        self.dring = dring

    def get(self, account_id, to):
        return jsonify({'call_id': self.dring.call.place_call(account_id, to)})

class Refuse(Resource):
    def __init__(self, dring):
        self.dring = dring

    def get(self, call_id):
        return jsonify({'refuse': self.dring.call.refuse(call_id)})

class Accept(Resource):
    def __init__(self, dring):
        self.dring = dring

    def get(self, call_id):
        return jsonify({'accept': self.dring.call.accept(call_id)})

class HangUp(Resource):
    def __init__(self, dring):
        self.dring = dring

    def get(self, call_id):
        return jsonify({'hang_up': self.dring.call.hang_up(call_id)})

class Hold(Resource):
    def __init__(self, dring):
        self.dring = dring

    def get(self, call_id):
        return jsonify({'hold': self.dring.call.hold(call_id)})

class Unhold(Resource):
    def __init__(self, dring):
        self.dring = dring

    def get(self, call_id):
        return jsonify({'unhold': self.dring.call.unhold(call_id)})
