from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import db, Progress

progress_routes = Blueprint("progress_routes", __name__)

@progress_routes.route('/progress', methods=['POST'])
@jwt_required()
def save_progress():
    users_id = get_jwt_identity()
    data = request.get_json()
    scene = data.get('scene')
    progress = Progress.query.filter_by(user_id=users_id).first()

    if progress:
        progress.scene = scene
    else:
        progress = Progress(user_id=users_id, scene=scene)
        db.session.add(progress)

    db.session.commit()
    return jsonify({"message": "Progress saved"}), 200

@progress_routes.route('/progress', methods=['GET'])
@jwt_required()
def load_progress():
    users_id = get_jwt_identity()
    progress = Progress.query.filter_by(user_id=users_id).first()
    if progress:
        return jsonify({"scene": progress.scene}), 200
    else:
        return jsonify({"scene": None}), 200
