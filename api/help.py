from bottle import request, get

@get('/')
def root():
    return '<a href="http://localhost:8080/user/">User API</a>'

