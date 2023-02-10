from flask import Blueprint, jsonify, request
from werkzeug.security import check_password_hash, generate_password_hash
from http.client import BAD_REQUEST, CONFLICT, CREATED, UNAUTHORIZED, OK
import validators, os, sys
path = os.getcwd()
sys.path.append(path+"/src/")
from backend import database as dbcons
from flask_jwt_extended import create_access_token,create_refresh_token, jwt_required, get_jwt_identity
from flasgger import swag_from
from dotenv import load_dotenv

load_dotenv()

auth = Blueprint("auth", __name__, url_prefix="/api/v2/auth")


@auth.post('/register')
@swag_from('./docs/auth/register.yaml')
def register():
    conn = dbcons.getConnection()
    cur = conn.cursor()

    username = request.json['username']
    email = request.json['email']
    password = request.json['password']

    # Validation checks
    if len(password) < 6:
        return jsonify({"error":"Password is too short!"}), BAD_REQUEST

    if len(username) < 3:
        return jsonify({"error":"Username is too short!"}), BAD_REQUEST

    if not username.isalnum() or " " in username:
        return jsonify({"error":"Username should be alphanumeric and not contain any spaces!"}), BAD_REQUEST

    if not validators.email(email):
        return jsonify({"error":"Email is not valid!"}), BAD_REQUEST

    ## Check to see if item is already in database 
    userTableName = os.environ['userTableName']
    cur.execute(f"select * from {userTableName} where username = %s", (username,))
    username_result = cur.fetchone()

    if username_result:
        return jsonify({"error" : "User with this username already exists!"}), CONFLICT

    cur.execute(f"select * from {userTableName} where email = %s", (email,))
    email_result = cur.fetchone()

    if email_result:
        return jsonify({"error" : "User with this email already exists!"}), CONFLICT

    pwd_hash = generate_password_hash(password)

    dbcons.addUser(username=username, email=email, pwd_hash=pwd_hash, userTableName=os.getenv('userTableName'))
    
    return jsonify({"message":"User Created!","user":{'username':username, 'email':email}}), CREATED

@auth.post('/login')
@swag_from('./docs/auth/login.yaml')
def login():
    conn = dbcons.getConnection()
    cur = conn.cursor()

    email = request.json.get('email','')
    password = request.json.get('password','')

    ## Check to see if item is already in database 
    userTableName = os.envrion['userTableName']
    cur.execute(f"select password from {userTableName} where email = %s", (email,))
    password_hash = cur.fetchone()[0]
    
    cur.execute(f"SELECT id FROM {userTableName} WHERE email = %s", (email,))
    user_id = cur.fetchone()[0]
    conn.commit()
    cur.close()
    conn.close()
    
    is_pass_correct = check_password_hash(password_hash, password)
    if is_pass_correct:
        refresh = create_refresh_token(identity=user_id)
        access = create_access_token(identity=user_id)

        return jsonify({
            'user' : {
                'email' : email,
                'refresh_token' : refresh,
                'access_token' : access
            }
        }), OK
    
    return jsonify({"error":"Wrong Credentials!"}), UNAUTHORIZED

@auth.get("/me")
@jwt_required()
@swag_from('./docs/auth/get_logged_in_user.yaml')
def me():
    user_id = get_jwt_identity()

    userTableName = os.environ['userTableName']

    conn = dbcons.getConnection()
    cur = conn.cursor()
    cur.execute(f"SELECT username FROM {userTableName} WHERE id = %s", (user_id,))
    username = cur.fetchone()[0]
    cur.execute(f"SELECT email FROM {userTableName} WHERE id = %s", (user_id,))
    email = cur.fetchone()[0]
    conn.commit()
    cur.close()
    conn.close()

    return jsonify({"username": username, "email": email}), OK

@auth.get("/token/refresh")
@jwt_required(refresh=True)
@swag_from('./docs/auth/get_refresh.yaml')
def refresh_token():   
    identity = get_jwt_identity()
    access = create_access_token(identity=identity)

    return jsonify({
        'access_token' : access
    }), OK
