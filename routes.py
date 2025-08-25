from flask import Blueprint, request, jsonify
from services import register_user, login_user

auth_routes = Blueprint("auth_routes", __name__)

@auth_routes.route("/register", methods=["POST"])
def register():
    data = request.get_json()
    return register_user(data["username"], data["email"], data["password"])

@auth_routes.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    return login_user(data["username"], data["password"])


