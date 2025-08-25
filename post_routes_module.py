from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import db, Post, User

post_routes = Blueprint("post_routes", __name__)

@post_routes.route('/posts', methods=['POST'])
@jwt_required()
def create_post():
    user_id = get_jwt_identity()
    data = request.get_json()
    content = data.get("content")
    if not content:
        return jsonify({"error": "Content is required"}), 400

    post = Post(content=content, user_id=user_id)
    db.session.add(post)
    db.session.commit()
    return jsonify({"message": "Post created"}), 201


@post_routes.route('/posts/<int:post_id>', methods=['PUT'])
@jwt_required()
def update_post(post_id):
    current_user_id = get_jwt_identity()
    post = Post.query.get_or_404(post_id)

    if post.user_id != current_user_id:
        return jsonify({"error": "You cannot update someone else's post silly"}), 403

    data = request.get_json()
    post.title = data.get('title', post.title)
    post.content = data.get('content', post.content)

    db.session.commit()
    return jsonify({"message": "Post updated"})


@post_routes.route('/posts/<int:post_id>', methods=['DELETE'])
@jwt_required()
def delete_post(post_id):
    current_user_id = get_jwt_identity()
    post = Post.query.get_or_404(post_id)

    if post.user_id != current_user_id:
        return jsonify({"error": "You cannot delete someone else's post silly"}), 403

    db.session.delete(post)
    db.session.commit()
    return jsonify({"message": "Post deleted"})

@post_routes.route('/posts', methods=['GET'])
def get_all_posts():
    posts = Post.query.all()
    result = []
    for post in posts:
        user = User.query.get(post.user_id)
        result.append({
            "id": post.id,
            "title": post.title,
            "content": post.content,
            "author": user.username if user else "Unknown"
        })
    return jsonify(result), 200
def get_posts():
    posts = Post.query.order_by(Post.id.desc()).all()
    return jsonify({"posts": [p.to_dict() for p in posts]})

@post_routes.route('/users', methods=['GET'])
def get_all_users():
    users = User.query.all()
    result = [{"id": user.id, "username": user.username} for user in users]
    return jsonify(result), 200