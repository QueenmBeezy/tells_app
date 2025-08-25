from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import db, User

profile_routes = Blueprint("profile_routes", __name__)

@profile_routes.route("/save-progress", methods=["POST"])
@jwt_required()
def save_progress():
    current_user_id = get_jwt_identity()
    data = request.get_json()
    progress = data.get("progress")

    user = User.query.get(current_user_id)
    user.saved_progress = progress
    db.session.commit()

    return jsonify({"message": "Progress saved!"}), 200

@profile_routes.route("/load-progress", methods=["GET"])
@jwt_required()
def load_progress():
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)
    return jsonify({"progress": user.saved_progress}), 200

@profile_routes.route("/profile/<string:username>", methods=["GET"])
def view_profile(username):
    user = User.query.filter_by(username=username).first()
    if not user:
        return jsonify({"error": "User not found"}), 404

    return jsonify({
        "username": user.username,
        "bio": user.bio if hasattr(user, "bio") else "",
        "progress": user.saved_progress if hasattr(user, "saved_progress") else "",
        "posts": [{"id": post.id, "content": post.content} for post in user.posts]
    }), 200

@profile_routes.route("/users", methods=["GET"])
def get_users():
    users = User.query.all()
    user_list = [{"id": u.id, "username": u.username} for u in users]
    return jsonify(user_list)
  
@profile_routes.route("/users/<int:user_id>", methods=["GET"])
def get_user_profile(user_id):
    user = User.query.get_or_404(user_id)
    return jsonify({"id": user.id, "username": user.username})


