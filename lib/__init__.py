'''from flask import Flask
from flask_restful import Resource, Api, reqparse, inputs
from flask_jwt import JWT
from flask_pymongo import PyMongo
from bson.json_util import dumps
import pymongo

from lib.security import authenticate, identity

app = Flask(__name__)
app.secret_key = 'qawzsx13'
app.config['MONGO_URI'] = "mongodb://127.0.0.1:27017/parkingdb"
app.config['MONGO_DBNAME'] = 'parkingdb'

mongo = PyMongo(app)
mongo.db.parking.create_index([('slot_id', pymongo.ASCENDING)], unique=True)
api = Api(app)

jwt = JWT(app, authenticate, identity) #/auth'''