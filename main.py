from flask import Flask, render_template
from flask_restful import Api, Resource, reqparse
import random
import json
from numpy import *

#setting up flask
app = Flask(__name__)
api = Api(app)

#reading stored array, allows for less junk in main.py and makes it easier to expand
with open('galaxy.txt', 'r') as filehandle:  
    galaxy = json.load(filehandle)

#class for specific galaxy fact
class GalaxySpecific(Resource):
    def get(self, id):
        for data in galaxy:
            if(id == data["id"]):
                return data, 200
        return "Fact not found", 404

#class for random galaxy fact
class GalaxyRandom(Resource):
    def get(self):
        return random.choice(galaxy)

#class for all galaxy facts
class GalaxyIndex(Resource):
    def get(self):
        return galaxy

@app.route('/')
def hello_world():
    return render_template('index.html')

api.add_resource(GalaxySpecific, "/galaxy/spec/<string:id>")
api.add_resource(GalaxyRandom, "/galaxy/rand/")
api.add_resource(GalaxyIndex, "/galaxy/index/")

app.run(host='0.0.0.0',port=8080)