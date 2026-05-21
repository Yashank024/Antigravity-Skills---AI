from flask import Blueprint, jsonify, request

user_bp = Blueprint('user', __name__)

@user_bp.route('/<int:user_id>', methods=['GET'])
def get_user(user_id):
    try:
        # mock DB call
        user = {"id": user_id, "name": "John Doe"}
        if not user:
            return jsonify({"error": "User not found"}), 404
        return jsonify(user), 200
    except Exception as e:
        return jsonify({"error": "Internal server error"}), 500
