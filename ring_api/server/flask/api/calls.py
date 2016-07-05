from flask import jsonify, request
from flask_restful import Resource

class Calls(Resource):
    def __init__(self, dring):
        self.dring = dring

    def put(self, call_id):
        data = request.get_json(force=True)

        if not 'action' in data:
            return jsonify({
                'status': 400,
                'message': 'action not found in request data'
            })

        if data['action'] in 'accept':
            return jsonify({
                'status': 200,
                'accept': self.dring.call.accept(call_id)
            })
        
        elif data['action'] in 'refuse':
            return jsonify({
                'status': 200,
                'refuse': self.dring.call.refuse(call_id)
            })
        
        elif data['action'] in 'hangup':
            return jsonify({
                'status': 200,
                'hang_up': self.dring.call.hang_up(call_id)
            })
        
        elif data['action'] in 'hold':
            return jsonify({
                'status': 200,
                'hold': self.dring.call.hold(call_id)
            })
        
        elif data['action'] in 'unhold':
            return jsonify({
                'status': 200,
                'unhold': self.dring.call.unhold(call_id)
            })
        
        else:
            return jsonify({
                'status': 400,
                'message': 'action not valid'
            })
