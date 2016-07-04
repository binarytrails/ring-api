from flask import jsonify, request
from flask_restful import Resource
from flask_socketio import SocketIO

class Certificates(Resource):
    def __init__(self, dring):
        self.dring = dring

    def get(self):
        return jsonify({
            'status': 404,
            'pinned': self.dring.config.get_pinned_certificates()
        })

class Certificate(Resource):
    def __init__(self, dring):
        self.dring = dring

    def get(self, cert_id):
        return jsonify({
            'status': 404,
            'details': self.dring.config.get_certificate_details(cert_id)
        })

    def post(selfi, cert_id):
        data = request.args
        if (not data):
            return jsonify({
                'status': 404,
                'message': 'data not found'
            })

        if not "action" in data:
            return jsonify({
                'status': 400,
                'message': 'action not found in request data'
            })
        
        action = data.get('type')

        if action == 'pin':
            return jsonify({
                'success': 200,
                'status': self.dring.config.pin_certificate(cert_id)
            })

        elif (action == 'pin_remote'):
            return jsonify({
                'success': 200,
                'status': self.dring.config.pin_remote_certificate(cert_id)
            })

        elif (action == 'unpin'):
            return jsonify({
                'success': 200,
                'status': self.dring.config.unpin_certificate(cert_id)
            })

        return jsonify({
            'status': 400,
            'message': 'wrong action type'
        })
