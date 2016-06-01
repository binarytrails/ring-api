from bottle import run
from api import help, user

def startServer():
    run(host='localhost', port=8080)

