from flask import Flask, render_template, redirect
from flask_restful import Api, Resource, reqparse
import random
import json
from numpy import *
from threading import Thread

#setting up flask
app = Flask(__name__)
api = Api(app)

#----------

#reading stored array, allows for less junk in main.py and makes it easier to expand
with open('galaxy.json', 'r') as filehandle:  
    galaxy = json.load(filehandle)


#----------

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

#----------

#routing to index page
@app.route('/')
def index():
    return render_template('index.html')

#routing to 404 page
@app.errorhandler(404)
def page_not_found(e):
    # note that we set the 404 status explicitly
    return render_template('404.html'), 404

#routing to the facts client
@app.route('/client/')
def client():
	return redirect("https://client.api.piemadd.com/", code=302)

#----------

#adding galaxy api resources
api.add_resource(GalaxySpecific, "/galaxy/spec/<string:id>")
api.add_resource(GalaxyRandom, "/galaxy/rand/")
api.add_resource(GalaxyIndex, "/galaxy/index/")

#----------

#running webserver
def run():
  app.run(host='0.0.0.0',port=8080)

def keep_alive():  
    t = Thread(target=run)
    t.start()

keep_alive()
