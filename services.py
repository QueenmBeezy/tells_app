from models import db, User
from flask_bcrypt import Bcrypt
from flask_jwt_extended import create_access_token

bcrypt = Bcrypt()

def register_user(username, password):
    if User.query.filter((User.username == username)).first():
        return {"error": "Username not unique"}, 409
    
    hashed_pw = bcrypt.generate_password_hash(password).decode('utf-8')
    user = User(username=username, password_hash=hashed_pw)
    db.session.add(user)
    db.session.commit()
    return {"message": "Successful registration!"}, 201

def login_user(username, password):
    user = User.query.filter_by(username=username).first()
    if user and bcrypt.check_password_hash(user.password_hash, password):
        access_token = create_access_token(identity=user.id)
        return {"access_token": access_token}, 200
    return {"error": "Invalid username or password"}, 401    
