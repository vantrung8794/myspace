from flask import Response, request
from flask_restful import Resource
from database.models import User
from database.db import mysql
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from commons.appuntils import hash_password, check_password
import json
import datetime

class SignUpAPI(Resource):
    def post(self):
        username = request.form["username"]
        password = request.form["password"]
        bcrypt_pass = hash_password(password)
        conn = mysql.connect()
        cursor =conn.cursor()
        cursor.execute("INSERT INTO users(username, password) VALUES (%s, %s)", (username, bcrypt_pass))
        cursor.connection.commit()
        cursor.close()
        return "Register " + username + " successfully!", 200

class LoginAPI(Resource):
    def post(self):
        username = request.form["username"]
        password = request.form["password"]
        conn = mysql.connect()
        cursor =conn.cursor()
        cursor.execute("SELECT password FROM users WHERE username = %s", (username))
        cursor.connection.commit()
        crypt_pass = cursor.fetchone()
        cursor.close()
        if crypt_pass is None:
            return {'error': 'User not exist'}, 401
        authenized = check_password(crypt_pass[0], password)
        if not authenized:
            return {'error': 'Username or Password invalid'}, 401
        expires = datetime.timedelta(days=7)
        access_token = create_access_token(identity=username, expires_delta=expires)
        return {'token': access_token}, 200

class ChangePasswordAPI(Resource):
    @jwt_required
    def put(self):
        username = get_jwt_identity()
        newpass = request.form["password"]
        bcrypt_pass = hash_password(newpass)
        conn = mysql.connect()
        cursor =conn.cursor()
        cursor.execute("UPDATE users SET password = %s WHERE username = %s", (bcrypt_pass ,username))
        cursor.connection.commit()
        cursor.close()
        return "Change password for " + username + " successfully!", 200