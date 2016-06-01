from bottle import request, response, get
import cgi, json

# Routes

user = '/user/'
userAction = '/user/<userId>/<action>/'

# Controllers

@get(user)
def hello():
    return ''.join(['Ask an action to <i>', cgi.escape(userAction), '</i>'])

@get(userAction)
def user(userId, action):
    #response.status = 400  # example
    response.headers['Content-Type'] = 'application/json'
    return json.dumps({userId: ' '.join([action, 'result'])})

