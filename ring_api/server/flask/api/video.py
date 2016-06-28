from flask import jsonify, request, abort
from flask_restful import Resource
from flask_socketio import SocketIO

class Devices(Resource):
    def __init__(self, dring):
        self.dring = dring

    def get(self):
        return jsonify({'devices': self.dring.video.devices()})

class Settings(Resource):
    def __init__(self, dring):
        self.dring = dring

    def get(self, device_name):
        return jsonify({'settings': self.dring.video.get_settings(device_name)})

    def put(self, device_name):
        data = request.get_json(force=True)

        return jsonify({'settings': self.dring.video.get_settings(device_name)})

class Default(Resource):
    def __init__(self, dring):
        self.dring = dring

    def get(self):
        return jsonify({'default': self.dring.video.get_default_device()})

    def put(self):
        data = request.get_json(force=True)
        
        if not "device" in data:
            return abort(400)
       
        self.dring.video.set_default_device(data["device"])

        return jsonify({'default': self.dring.video.get_default_device()})

class Start(Resource):
    def __init__(self, dring):
        self.dring = dring

    def get(self):
        self.dring.video.start_camera()

        return jsonify({'camera': self.dring.video.has_camera_started()})

class Stop(Resource):
    def __init__(self, dring):
        self.dring = dring

    def get(self):
        self.dring.video.stop_camera()

        return jsonify({'camera': self.dring.video.has_camera_started()})

class Switch(Resource):
    def __init__(self, dring):
        self.dring = dring

    def put(self):
        data = request.get_json(force=True)
        
        if not "input" in data:
            return abort(400)
        
        return jsonify({'switched': self.dring.video.switch_input(data["input"])})

class Status(Resource):
    def __init__(self, dring):
        self.dring = dring

    def get(self):
        return jsonify({'camera': self.dring.video.has_camera_started()})
