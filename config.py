import os

class Config:
    SQLALCHEMY_DATABASE_URI = 'sqlite:///tells.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.environ.get("BUTLERTELLS_KEY", "butlertells")
    JWT_SECRET_KEY = os.environ.get("JWT_SECRET_KEY", "jwtsk")