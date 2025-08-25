from flask import Flask
from config import Config
from models import db
from services import bcrypt
from routes import auth_routes
from post_routes_module import post_routes
from flask_jwt_extended import JWTManager
from profile_routes_module import profile_routes
from routes import progress_routes


app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)
bcrypt.init_app(app)
JWTManager(app)

app.register_blueprint(progress_routes, url_prefix="/api")
app.register_blueprint(auth_routes, url_prefix='/api')
app.register_blueprint(post_routes, url_prefix='/api/posts')
app.register_blueprint(profile_routes, url_prefix='/api')

with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)
