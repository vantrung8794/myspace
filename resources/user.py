from flask import Response, request
from flask_restful import Resource
from database.models import User
from database.db import mysql
from flask_jwt_extended import jwt_required, get_jwt_identity
import json

class GetUserInfoAPI(Resource):
    @jwt_required
    def get(self):
        username = get_jwt_identity()
        conn = mysql.connect()
        cursor =conn.cursor()
        cursor.execute("SELECT username, avatar_url, fullname, package_id FROM users WHERE username = '%s'" % (username))
        cursor.connection.commit()
        user_tuple = cursor.fetchone()
        cursor.close()
        conn2 = mysql.connect()
        cursor2 =conn2.cursor()
        cursor2.execute("SELECT package_id, package_name, package_cost, package_data FROM packages WHERE package_id = %d" % (user_tuple[3]))
        cursor2.connection.commit()
        package = cursor2.fetchone()
        user = User(user_tuple[0], user_tuple[1], user_tuple[2], user_tuple[3], package[1], package[2], package[3])
        cursor2.close()
        json_data =  json.dumps({"userinfo": user.__dict__})
        return Response(json_data, mimetype = 'application/json', status=200)

