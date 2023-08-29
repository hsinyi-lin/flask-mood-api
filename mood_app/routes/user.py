from flask import Blueprint, request
from werkzeug.security import generate_password_hash, check_password_hash
import jwt 

import datetime

from ..extensions import mongo
from ..utils.response import *
from ..models.user import UserModel


user = Blueprint('user', __name__)

@user.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    
    user_col = mongo.db.user
    user = user_col.find_one({'email': data['email']})

    if user:
        return error_response('帳號已存在'), 400
    
    hash_pw = generate_password_hash(data['password'], method='sha256')
    new_user = UserModel.create_user(user_col, data, hash_pw)

    return success_response(new_user), 200


@user.route('/login', methods=['POST'])
def login():
    data = request.get_json()

    user_col = mongo.db.user
    user = user_col.find_one({'email': data['email']})

    if not user:
        return error_response('尚未註冊'), 400
    
    user_exist = check_password_hash(user['password'], data['password'])
    if not user_exist:
        return error_response('帳號或密碼錯誤'), 400
    
    token = jwt.encode({
        'email': data['email'],
        'expiration': str(datetime.datetime.utcnow() + datetime.timedelta(days=15))
    },'key', algorithm='HS256')

    # print(jwt.decode(token, 'key', algorithms=['HS256']))

    return success_response({'token': token}), 200

