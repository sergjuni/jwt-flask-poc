from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from .auth_utils import register_user_util, authenticate_user_util, users_db

auth_bp = Blueprint('auth_bp', __name__, url_prefix='/auth')

@auth_bp.route('/register', methods=['POST'])
def register():
  data = request.get_json()
  username = data.get('username')
  password = data.get('password')
  if not username or not password:
    return jsonify({"msg": "Username and Password are required"}), 400

  user = register_user_util(username, password)
  if user is None:
      return jsonify({"msg": "User already exists"}), 409

  return jsonify({"msg": "User registered successfully", "id": user['id']}), 201

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({"msg": "Username and Password are required"}), 400

    user = authenticate_user_util(username, password)
    print(user)
    if not user:
        return jsonify({"msg": "Invalid Credentials"}), 401

    identity_para_token = user['username']
    print(f"DEBUG NA CRIAÇÃO DO TOKEN: Identidade='{identity_para_token}', Tipo={type(identity_para_token)}")

    access_token = create_access_token(identity=identity_para_token)
    return jsonify(access_token=access_token), 200


@auth_bp.route('/protected', methods=['GET'])
@jwt_required()
def protected():
    current_user_username = get_jwt_identity()
    user_data = users_db.get(current_user_username)
    if not user_data:
        return jsonify({"msg": "User Token not found"}), 404

    return jsonify(
        logged_in_as=current_user_username,
        user_id=user_data['id']
    ), 200
