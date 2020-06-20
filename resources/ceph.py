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

access_key = 'DGZ3M9S7TC2MW9M37AK4'
secret_key = '3thIb8rhcmSF79mMCPbqM9MGvGlJt3Ilqu3BsjfB'

conn = boto.connect_s3(
        aws_access_key_id = access_key,
        aws_secret_access_key = secret_key,
        host = 's3.oanhdt.xyz',
        # is_secure=False,               # uncomment if you are not using ssl
        calling_format = boto.s3.connection.OrdinaryCallingFormat(),
        )

class UploadAPI(Resource):
    def post(self):
        bucket = conn.get_bucket("newfiles", validate=False)
        k = Key(bucket)
        k.key = 'foobar2.txt'
        k.set_contents_from_string('This is a test of S3')
        return "save file successfully!", 200

class DeleteContentAPI(Resource):
    def delete(self, filename):
        bucket = conn.get_bucket("newfiles", validate=False)
        bucket.delete_key(filename)
        return "delete %s successfully!" % filename, 200

class CreateBucketAPI(Resource):
    # @jwt_required
    def post(self):
        bucket_name = request.form['bucketname']
        bucket = conn.create_bucket('bucket_name')
        if bucket is None:
            return {"error": "Tao bucket that bai"}, 400
        return 'Tạo bucket ' + bucket_name + ' thành công', 200

class GetListBucket(Resource):
    def get(self):
        for bucket in conn.get_all_buckets():
            print("Bucket - %s - %s" % (bucket.name, bucket.creation_date))
            for key in bucket.list():
                print("file: %s %s %s" %(key.name, key.size, key.last_modified)) 
        return "list bucket ok", 200

class GetURLForFile(Resource):
    def get(self, filename):
        my_bucket = conn.get_bucket("newfiles", validate=False)
        my_key = my_bucket.get_key(filename)
        my_url = my_key.generate_url(36000, query_auth=True, force_http=False)
        return {"url": my_url}, 200