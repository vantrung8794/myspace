from flaskext.mysql import MySQL

mysql = MySQL()

def initialize_db(app): 
    mysql.init_app(app)