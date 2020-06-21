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
import datetime
from werkzeug.utils import secure_filename

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
    def post(self):
        my_url = ""
        if 'file' not in request.files:
            return {"error": "Không tìm thấy file"}, 400
        file = request.files['file']
        if file.filename == '':
            return {"error": "Không tìm thấy file"}, 400
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            k = Key(bucket)
            k.key=filename
            k.set_contents_from_file(file)
            k.set_acl('public-read')
            my_url = k.generate_url(expires_in=0, query_auth=False, force_http=False) 
        return {"url": my_url}, 200

class DeleteContentAPI(Resource):
    def delete(self, filename):
        bucket.delete_key(filename)
        return "delete %s successfully!" % filename, 200

class CreateBucketAPI(Resource):
    # @jwt_required
    def post(self):
        bucket_name = request.form['bucketname']
        my_bucket = conn.create_bucket('bucket_name')
        if my_bucket is None:
            return {"error": "Tao bucket that bai"}, 400
        return 'Tạo bucket ' + bucket_name + ' thành công', 200

class GetListBucket(Resource):
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
        res = {"items": list_item}
        return Response(json.dumps(res), mimetype = 'application/json', status=200)

class GetURLForFile(Resource):
    def get(self, filename):
        my_key = bucket.get_key(filename)
        my_url = my_key.generate_url(expires_in=0, query_auth=False, force_http=False) 
        return {"url": my_url}, 200