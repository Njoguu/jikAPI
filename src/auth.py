from flask import Blueprint, request, jsonify
from werkzeug.security import check_password_hash, generate_password_hash
import re
from src.database import User, db
from http import HTTPStatus


auth = Blueprint("auth", __name__,
url_prefix="/api/v1/auth")

@auth.post('/register')
def register_user():
    username=request.json['username']
    email=request.json['email']
    password=request.json['password']

    regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'

    if len(password) < 6:
        return jsonify({"Error!" : "Password is too short!"}), HTTPStatus.BAD_REQUEST

    if len(username) < 4:
        return jsonify({"Error!" : "Username is too short!"}), HTTPStatus.BAD_REQUEST

    if not username.isalnum() or " " in username:
        return jsonify({'Error!' : 'Username should be alphanumeric and should not have any spaces!'}), HTTPStatus.BAD_REQUEST

    if (re.fullmatch(regex, email)) == False:
        return jsonify({'Error' : 'Invalid email address!'}), HTTPStatus.BAD_REQUEST

    if User.query.filter_by(email=email).first() is not None:
        return jsonify({"Error" : "A user with this email already exists!"}), HTTPStatus.CONFLICT

    if User.query.filter_by(username=username).first() is not None:
        return jsonify({"Error" : "A user with this username already exists!"}), HTTPStatus.CONFLICT

    # Hash user's password
    pwd_hash =  generate_password_hash(password)

    # Save user to DB
    user=User(username=username, password=pwd_hash, email=email)
    db.session.add(user)
    db.session.commit()

    return jsonify({
        'Message' : 'User Created!',
        'user' : {
            'username' : username,
            'email' : email
        }
    }), HTTPStatus.CREATED



@auth.get("/me")
def me():
    return {'user': 'me'}
