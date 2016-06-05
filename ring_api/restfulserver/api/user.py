from bottle import request, response, post, get
import cgi, json

api = {
    'routes' : '/user/routes/',
    'accounts' : '/user/accounts/'
}

class User:
    def __init__(self, _dring):
        global dring
        dring = _dring

    def api():
        return api

@get(api['routes'])
def routes():
    return json.dumps(api)

@get(api['accounts'])
def accounts():
    return json.dumps(dring.config.accounts())

