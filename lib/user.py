from lib.app import *
from werkzeug.security import safe_str_cmp
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
)
from lib.MyLogger import setup_custom_logger

ULog = setup_custom_logger('userlog')

class Admin:
    global mongo

    def __init__(self, _id, username, password):
        self.id = _id
        self.username = username
        self.password = password

    @classmethod
    def find_by_username(cls, username):
        return mongo.db.administrator.find_one({'username': username})

    @classmethod
    def find_by_id(cls, uid):
        return mongo.db.administrator.find_one({'uid': uid})


class AdminLogin(Resource):
    global mongo
    global jwt
    parser = reqparse.RequestParser()
    parser.add_argument( 'username',
                         type = str,
                         required = True,
                         help = "Username cannot be blank"
                        )
    parser.add_argument( 'password',
                         type = str,
                         required = True,
                         help = "Password cannot be blank"
                        )
    def post(self):
        data = self.parser.parse_args()
        admin_dict = Admin.find_by_username(data['username'])
        ULog.info("admin_dict: %s, admin_dict type: %s" % (admin_dict, type(admin_dict)))
        if admin_dict.get('username', None) and safe_str_cmp(admin_dict.get('password'), data['password']):
            access_token = create_access_token(identity=admin_dict.get('uid'), fresh=True)
            refresh_token = create_refresh_token(admin_dict.get('uid'))
            return {
                'access_token': access_token,
                'refresh_token': refresh_token
            }, 200

        return {'message': 'Invalid credentials'}, 401

