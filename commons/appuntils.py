from flask_bcrypt import generate_password_hash, check_password_hash

def hash_password(password):
    return generate_password_hash(password).decode('utf8')
    
def check_password(bcrypt_password, password):
    print(bcrypt_password, password)
    return check_password_hash(bcrypt_password, password)