from .user import GetUserInfoAPI
from .auth import SignUpAPI, LoginAPI, ChangePasswordAPI
from .ceph import UploadAPI, CreateBucketAPI, GetListBucket, DeleteContentAPI, GetURLForFile, GetCountData, GetHistoryData

def initialize_routes(api):
    api.add_resource(GetUserInfoAPI, '/getuserinfo')
    api.add_resource(SignUpAPI,'/signup')
    api.add_resource(LoginAPI,'/login')
    api.add_resource(ChangePasswordAPI,'/changepassword')
    api.add_resource(UploadAPI, '/upload')
    api.add_resource(DeleteContentAPI,'/deletefile/<filename>')
    api.add_resource(CreateBucketAPI, '/createbucket')
    api.add_resource(GetListBucket, '/getlistbucket')
    api.add_resource(GetURLForFile, '/geturlforfile/<filename>')
    api.add_resource(GetCountData, '/getcountdata')
    api.add_resource(GetHistoryData, '/gethistory')
