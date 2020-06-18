from flask import Flask
from flask_restful import Api
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from resources.routes import initialize_routes
from database.db import initialize_db


app = Flask(__name__)
api = Api(app)
bcrypt = Bcrypt(app)

app.config.from_envvar('ENV_FILE_LOCATION')
# export ENV_FILE_LOCATION=./.env

initialize_db(app)
initialize_routes(api)
jwt = JWTManager(app)

if __name__ == "__main__":
    app.run()