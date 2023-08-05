#coding=utf-8
import time, sys, cherrypy, os
import argparse
import yaml
from paste.translogger import TransLogger
from app import create_app
import flask_profiler
cherrypy.log.error_log.propagate = False
cherrypy.log.access_log.propagate = False
class FireflyError(Exception):
    pass
def parse_args():
    p = argparse.ArgumentParser()
    p.add_argument("-t", "--token", help="token to authenticate the requests")
    p.add_argument("-b", "--bind", dest="ADDRESS", default="127.0.0.1:8000")
    p.add_argument("-c", "--config", dest="config_file", default=None)
    p.add_argument("functions", nargs='*', help="functions to serve")
    return p.parse_args()
def parse_config_file(config_file):
    if not os.path.exists(config_file):
        raise FireflyError("Specified config file does not exist..")
    with open(config_file) as f:
        config_dict = yaml.safe_load(f)
    return config_dict

def parse_config_data(config_dict):
    functions = [f["function"]
            for name, f in config_dict["functions"].items()]
    token = config_dict.get("token", None)
    return functions, token

class Microservices(object):
    """
    Allow creation of predict and other microservices
    aws_key : str, optional
       aws key
    aws_secret : str, optional
       aws secret
    """
    def __init__(self,aws_key=None,aws_secret=None):
        self.aws_key = aws_key
        self.aws_secret = aws_secret
    def run_server(self,app,port=5412,host='127.0.0.1'):
        # Enable WSGI access logging via Paste
        app_logged = TransLogger(app)
 
        # Mount the WSGI callable object (app) on the root directory
        cherrypy.tree.graft(app_logged, '/')
 
        # Set the configuration of the web server
        cherrypy.config.update({
            'engine.autoreload.on': True,
            'log.screen': True,
            'server.socket_port': port,
            'server.socket_host': '%s'%(host)
        })
 
        # Start the CherryPy WSGI web server
        cherrypy.engine.start()
        cherrypy.engine.block()
 

    def create_prediction_microservice(self,model_list,yml_conf=False,port=5412,host='127.0.0.1'):
        """
        Create a prediction Flask/cherrypy microservice app
        Parameters
        ----------
        func_name : list
           location of pipeline
        model_name : str
           model name to use for this pipeline
        """
        
        #函数来自配置文件
        if yml_conf:
            function_specs, token = parse_config_data(parse_config_file(yml_conf))
        else:
            function_specs=model_list
        app = create_app(function_specs)
        app.config['flask_profiler']={"enabled": True,"storage": {"engine": "mongodb"},"basicAuth":{"enabled": True,"username": "leepand","password":"admin"},"ignore": ["^/static/.*"]}
        flask_profiler.init_app(app)
        # start web server
        self.run_server(app,port,host)