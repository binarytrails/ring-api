from flask import jsonify, request, abort
from flask_restful import Resource
from flask_socketio import SocketIO

class VideoDevices(Resource):
    def __init__(self, dring):
        self.dring = dring

    def get(self):
        data = request.args
        if (not data):
            return abort(404, {
                'dev_message': 'data not found'
            })

        elif ('type' not in data):
            return jsonify({
                'status': '404',
                'dev_message': 'type not found in data'
            })
        
        device_type = data.get('type')

        if (device_type == 'all'):
            return jsonify({'devices': self.dring.video.devices()})

        elif (device_type == 'default'):
            return jsonify({'default': self.dring.video.get_default_device()})

        return abort(404, {
            'dev_message': 'wrong device type'
        })

    def put(self):
        data = request.args
        if (not data):
            return abort(404, {
                'dev_message': 'data not found'
            })

        elif ('type' not in data):
            return abort(404, {
                'dev_message': 'type not found in data'
            })
        
        device_type = data.get('type')

        if (device_type == 'default'):
            data = request.get_json(force=True)

            if not "device" in data:
                return abort(400, {
                    'dev_message': 'device not found in request data'
                })
           
            self.dring.video.set_default_device(data["device"])

            return jsonify({'default': self.dring.video.get_default_device()})

        return abort(400, {
            'dev_message': 'wrong device type'
        })

class VideoSettings(Resource):
    def __init__(self, dring):
        self.dring = dring

    def get(self, device_name):
        return jsonify({'settings': self.dring.video.get_settings(device_name)})

    def put(self, device_name):
        data = request.get_json(force=True)

        return jsonify({'settings': self.dring.video.get_settings(device_name)})

class VideoCamera(Resource):
    def __init__(self, dring):
        self.dring = dring

    def get(self):
        return jsonify({'camera': self.dring.video.has_camera_started()})
    
    def put(self):
        data = request.args
        if (not dat):
            return abort(404, {
                'dev_message': 'data not found'
            })

        elif ('action' not in data):
            return abort(404, {
                'dev_message': 'action not found in data'
            })
        
        device_type = data.get('type')

        if (device_type == 'start'):
           
            self.dring.video.start_camera()

            return jsonify({
                'cameraStatus': self.dring.video.has_camera_started()
            })
        
        elif (device_type == 'stop'):
           
            self.dring.video.stop_camera()

            return jsonify({
                'cameraStatus': self.dring.video.has_camera_started()
            })

        return abort(404, {
            'dev_message': 'wrong camera action'
        })
