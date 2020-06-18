from flask import Response, request
from flask_restful import Resource
from database.models import User
from database.db import mysql
import json

class UsersAPI(Resource):
    def get(self):
        conn = mysql.connect()
        cursor =conn.cursor()
        cursor.execute("SELECT * FROM users")
        cursor.connection.commit()
        users = cursor.fetchall()
        list_users = []
        for user_tuple in users:
            user = User(user_tuple[1], user_tuple[2])
            list_users.append(user)
        cursor.close()
        json_data =  json.dumps([user.__dict__ for user in list_users])
        return Response(json_data, mimetype = 'application/json', status=200)

