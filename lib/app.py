from flask import Flask
from flask_restful import Resource, Api, reqparse, inputs
from flask_jwt_extended import JWTManager, jwt_required
from flask_pymongo import PyMongo
from bson.json_util import dumps
from pymongo import ASCENDING, TEXT
from lib.MyLogger import *


app = Flask(__name__)
app.secret_key = 'qawzsx13'
app.config['MONGO_URI'] = "mongodb://my_mongo_container:27017/parkingdb"
app.config['MONGO_DBNAME'] = 'parkingdb'
app.config['PROPAGATE_EXCEPTIONS'] = True

mongo = PyMongo(app)
if mongo.db.administrator.find({'username': 'admin'}).count() != 1:
    mongo.db.administrator.insert_one(
        {'username': 'admin', 'password': 'admin123'})
mongo.db.parking.create_index([('slot_id', ASCENDING)], unique=True)
mongo.db.administrator.create_index([('username', TEXT)], unique=True)
api = Api(app)

ALog = setup_custom_logger("applog")

try:
    ALog.info("Initializing JWTManager...")
    jwt = JWTManager(app)
except Exception as fault:
    ALog.error("Error initializing JWT: %s" % fault)


class Slots(Resource):
    @jwt_required
    def get(self):
        slots = dumps(mongo.db.parking.find())
        return {'slots': slots}


class Slot(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('available',
                        type=inputs.boolean,
                        required=True,
                        help='This value makes the slot available or not available')

    @jwt_required
    def get(self, id):
        print("id: %s, id type: %s" % (id, type(id)))
        if mongo.db.parking.find({'slot_id': id}).count() == 0:
            return {}, 404
        else:
            slot = dumps(mongo.db.parking.find({'slot_id': id}))
            return {'slots': slot}, 200

    @jwt_required
    def post(self, id):  # This creates a new slot
        data = Slot.parser.parse_args()
        slot = {'slot_id': id, 'available': data['available']}
        print("slot:", slot)
        # Indexing is enabled for mongodb so duplicate entries
        # won't be added. Not checking here, directly adding.
        mongo.db.parking.insert_one(dict(slot))
        return slot, 201

    @jwt_required
    def delete(self, id):
        slot = {'slot_id': id}
        if mongo.db.parking.find({'slot_id': id}).count() == 0:
            return {'message': 'Slot with id {} does not exist'.format(id)}, 404
        else:
            mongo.db.parking.delete_one(dict(slot))
            return {'message': 'Slot with id {} deleted'.format(id)}

    @jwt_required
    def put(self, id):
        data = Slot.parser.parse_args()
        slot = {'slot_id': id, 'available': data['available']}
        if mongo.db.parking.find({'slot_id': id}).count() == 1:
            mongo.db.parking.update_one(
                {'slot_id': 1}, {'$set': {'available': data['available']}})
        else:
            mongo.db.parking.insert_one(dict(slot))
        return slot
