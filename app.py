from flask import Flask
from flask_restful import Api
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from resources.routes import initialize_routes
from database.db import initialize_db


app = Flask(__name__)
api = Api(app)
bcrypt = Bcrypt(app)

app.config['JWT_SECRET_KEY'] = 'myspace'
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = '12345678'
app.config['MYSQL_DATABASE_DB'] = 'myspace'
app.config['MYSQL_DATABASE_Host'] = 'localhost'

# app.config.from_envvar('ENV_FILE_LOCATION')
# export ENV_FILE_LOCATION=./.env

initialize_db(app)
initialize_routes(api)
jwt = JWTManager(app)

if __name__ == "__main__":
    app.run()