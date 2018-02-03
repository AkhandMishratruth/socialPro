from flask import Flask, render_template, request, jsonify 
from werkzeug import secure_filename
from PIL import Image
import os
import requests
import json
import yaml
import argparse
import sys
from postFB import *
import pickle
from multiprocessing import Value

counter = Value('i', -5)

project_root = os.path.dirname(__file__)
template_path = os.path.join(project_root, 'templates')
face = Flask(__name__, template_folder=template_path)

@face.route('/')
def hello_world():
    return "Welcome to FB API "

@face.route('/temp')
def tempJson():
    fil = open('tempJson.pickle', 'r')
    tempJsonString = pickle.load(fil)
    fil.close()
    
    return jsonify(listArray=tempJsonString)

@face.route('/json')
def jsonProvider():
    with counter.get_lock():
        counter.value = (counter.value + 10)%35
        print counter.value
    with face.app_context():
        toReturn = posts(counter.value)
        #print toReturn
        return toReturn
    
if __name__ == '__main__':
    face.run(host='0.0.0.0')
