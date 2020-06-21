import os
from flask import Response, request
from flask_restful import Resource
from database.db import mysql
from flask_jwt_extended import jwt_required, get_jwt_identity
import json
import logging
import boto
import boto.s3.connection
from boto.s3.key import Key
from datetime import datetime
from werkzeug.utils import secure_filename
from database.models import FileInfo
from decimal import Decimal
from commons.decima import CustomJSONEncoder

access_key = 'DGZ3M9S7TC2MW9M37AK4'
secret_key = '3thIb8rhcmSF79mMCPbqM9MGvGlJt3Ilqu3BsjfB'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'mp3'}

conn = boto.connect_s3(
        aws_access_key_id = access_key,
        aws_secret_access_key = secret_key,
        host = 's3.oanhdt.xyz',
        # is_secure=False,               # uncomment if you are not using ssl
        calling_format = boto.s3.connection.OrdinaryCallingFormat(),
        )

bucket = conn.get_bucket("newfiles", validate=False)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS 

class UploadAPI(Resource):
    @jwt_required
    def post(self):
        username = get_jwt_identity()
        my_urls = []
        files = request.files.getlist("file")
        for file in files:
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                k = Key(bucket)
                k.key=filename
                k.set_contents_from_file(file)
                k.set_acl('public-read')
                my_url = k.generate_url(expires_in=0, query_auth=False, force_http=False)
                now = datetime.now()
                formatted_date = now.strftime('%Y-%m-%d %H:%M:%S')
                # save file record to sql
                mysql_conn = mysql.connect()
                cursor = mysql_conn.cursor()
                query = "INSERT INTO files(file_name, file_size, file_url, created_date, user_name) \
                    VALUES('%s', %d, '%s', '%s', '%s')" % (filename, k.size, my_url, formatted_date, username)
                cursor.execute(query)
                cursor.connection.commit()
                cursor.close()
                my_urls.append({"name": filename ,"url": my_url})
        return Response(json.dumps(my_urls), mimetype = 'application/json', status=200)

class DeleteContentAPI(Resource):
    @jwt_required
    def delete(self, filename):
        user_name = get_jwt_identity()
        mysql_conn = mysql.connect()
        cursor = mysql_conn.cursor()
        cursor.execute("DELETE FROM files WHERE user_name = '%s' and file_name = '%s'" % (user_name,filename))
        cursor.connection.commit()
        cursor.close()
        bucket.delete_key(filename)
        return "delete %s successfully!" % filename, 200

class CreateBucketAPI(Resource):
    @jwt_required
    def post(self):
        bucket_name = request.form['bucketname']
        my_bucket = conn.create_bucket('bucket_name')
        if my_bucket is None:
            return {"error": "Tao bucket that bai"}, 400
        return 'Tạo bucket ' + bucket_name + ' thành công', 200

class GetListBucket(Resource):
    @jwt_required
    def get(self):
        user_name = get_jwt_identity()
        mysql_conn = mysql.connect()
        cursor = mysql_conn.cursor()
        cursor.execute("SELECT file_name, file_size, file_url, created_date, user_name FROM files WHERE user_name = '%s'" % (user_name))
        cursor.connection.commit()
        list_files = cursor.fetchall()
        list_items = []
        for file_info in list_files:
            file_item = FileInfo(file_info[0], file_info[1], file_info[2], file_info[3].strftime("%m/%d/%Y, %H:%M:%S"), file_info[4])
            list_items.append(file_item)
        cursor.close()
        json_data =  json.dumps({"files": [i.__dict__ for i in list_items]})
        return Response(json_data, mimetype = 'application/json', status=200)

class GetCountData(Resource):
    @jwt_required
    def get(self):
        user_name = get_jwt_identity()
        mysql_conn = mysql.connect()
        cursor = mysql_conn.cursor()
        cursor.execute("SELECT SUM(file_size) FROM files WHERE user_name = '%s'" % (user_name))
        cursor.connection.commit()
        count_data = cursor.fetchone()[0]
        return Response(json.dumps({'countdata': count_data}, cls=CustomJSONEncoder), mimetype = 'application/json', status=200)

class GetHistoryData(Resource):
    @jwt_required
    def get(self):
        user_name = get_jwt_identity()
        mysql_conn = mysql.connect()
        cursor = mysql_conn.cursor()
        cursor.execute("SELECT file_name, file_size, file_url, created_date, user_name FROM files WHERE user_name = '%s' ORDER BY created_date DESC LIMIT 5" % (user_name))
        cursor.connection.commit()
        list_files = cursor.fetchall()
        list_items = []
        for file_info in list_files:
            file_item = FileInfo(file_info[0], file_info[1], file_info[2], file_info[3].strftime("%m/%d/%Y, %H:%M:%S"), file_info[4])
            list_items.append(file_item)
        cursor.close()
        json_data =  json.dumps({"files": [i.__dict__ for i in list_items]})
        return Response(json_data, mimetype = 'application/json', status=200)


class GetListBucketFromS3(Resource):
    @jwt_required
    def get(self):
        list_item = []
        for bucket in conn.get_all_buckets():
            for key in bucket.list():
                item = {
                    "name": key.name,
                    "size": key.size,
                    "url": key.generate_url(expires_in=0, query_auth=False, force_http=False) 
                }
                list_item.append(item)
        res = {"files": list_item}
        return Response(json.dumps(res), mimetype = 'application/json', status=200)

class GetURLForFile(Resource):
    @jwt_required
    def get(self, filename):
        my_key = bucket.get_key(filename)
        my_url = my_key.generate_url(expires_in=0, query_auth=False, force_http=False) 
        return {"url": my_url}, 200