import json

from bottle import request, get

from ring_api.restfulserver.api import ring, user

api = {
    'root': '/',
    'routes': '/routes/',
}

class Root:
    def __init__(self, _dring):
        global dring
        dring = _dring

    def api():
        return api

@get(api['root'])
def root():
    return json.dumps(api)

@get(api['routes'])
def routes():
    ring_api = ring.Ring.api()
    user_api = user.User.api()
    return json.dumps({**api, **ring_api, **user_api})

