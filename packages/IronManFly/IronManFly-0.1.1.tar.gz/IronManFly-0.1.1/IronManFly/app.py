from flask import Blueprint
from flask import json
from flask import request
from algo_engine import AlgoEngine
import logging
import threading
#import auth

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
main = Blueprint('main', __name__)
ctx = threading.local()
ctx.request = None

from flask import Flask, request
from functools import wraps
from flask import jsonify
'''
@main.route("/predict/<function>", methods=["POST"])
def predict(function):
    ctx.request = request
    logger.debug("Model name %s ", function)
    req=json.dumps(request.json)
    top_ratings = recommendation_engine.call_func('/s',x=1,y=2)%(function)
    ctx.request = None
    return json.dumps(top_ratings)
'''

def check_auth(username, password):
    return username == 'admin' and password == 'secret'

def authenticate():
    message = {'message': "Not Authenticate."}
    resp = jsonify(message)

    resp.status_code = 401
    resp.headers['WWW-Authenticate'] = 'Basic realm="Example"'

    return resp

def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not auth: 
            return authenticate()

        elif not check_auth(auth.username, auth.password):
            return authenticate()
        return f(*args, **kwargs)

    return decorated

@main.route("/predict/<function>", methods = ["POST"])
@requires_auth
def api_predict_func(function):
    ctx.request = request
    if request.headers['Content-Type'] == 'text/plain':
        req_data=request.data
    elif request.headers['Content-Type'] == 'application/json':
        req_data=json.dumps(request.json)
    else:
        req_data='some thing wrong!'
    fun_name=('/%s')%(str(function).decode('utf-8'))
    fun_path=fun_name
    result=algo_engine.call_func(fun_path,**request.json)
    ctx.request = None
    return result
    #recommendation_engine.add_ratings(ratings)
@main.route('/info', methods = ['GET'])
def api_info():
    ctx.request = request
    #path = request.path_info
    if request.headers['Content-Type'] == 'text/plain':
        return "Text Message: " + request.data

    elif request.headers['Content-Type'] == 'application/json':
        return "WANDA_ML Server Message: " + json.dumps(request.json)

    elif request.headers['Content-Type'] == 'application/octet-stream':
        f = open('./binary', 'wb')
        f.write(request.data)
        f.close()
        return "Binary message written!"

    else:
        return "415 Unsupported Media Type ;)"
@main.route('/messages', methods = ['POST'])
def api_message():
    ctx.request = request
    #path = request.path_info
    if request.headers['Content-Type'] == 'text/plain':
        return "Text Message: " + request.data

    elif request.headers['Content-Type'] == 'application/json':
        return "JSON Message: " + json.dumps(request.json)

    elif request.headers['Content-Type'] == 'application/octet-stream':
        f = open('./binary', 'wb')
        f.write(request.data)
        f.close()
        return "Binary message written!"

    else:
        return "415 Unsupported Media Type ;)"

def create_app(function_specs):
    global algo_engine 

    algo_engine = AlgoEngine(function_specs)    
    
    app = Flask(__name__)
    app.register_blueprint(main)


    
    return app 
