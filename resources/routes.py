from .user import UsersAPI
from .auth import SignUpAPI, LoginAPI, ChangePasswordAPI

def initialize_routes(api):
    api.add_resource(UsersAPI, '/users')
    api.add_resource(SignUpAPI,'/signup')
    api.add_resource(LoginAPI,'/login')
    api.add_resource(ChangePasswordAPI,'/changepassword')
