#!/usr/bin/python3
"""
Create a new view for User objects that handles all default REST API actions
"""
from flask import jsonify, abort, request
from api.v1.views import app_views
from models import storage
from models.user import User


@app_views.route('/users', methods=['GET'], strict_slashes=False)
def get_users():
    """Retrieves the list of all User objects"""
    users = storage.all(User).values()
    users_list = [user.to_dict() for user in users]
    return jsonify(users_list)


@app_views.route('/users/<user_id>', methods=['GET'], strict_slashes=False)
def get_user(user_id):
    """Retrieves a User object"""
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    return jsonify(user.to_dict())


@app_views.route('/users/<user_id>', methods=['DELETE'], strict_slashes=False)
def delete_user(user_id):
    """Deletes a User object"""
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    storage.delete(user)
    storage.save()
    return jsonify({}), 200


@app_views.route('/users', methods=['POST'], strict_slashes=False)
def create_user():
    """Creates a User"""
    try:
        data = request.get_json()
    except Exception as e:
        abort(400, "Not valid JSON")


    if not data:
        abort(400, "Not a JSON")
    if "email" not in data:
        abort(400, "Missing email")
    if "password" not in data:
        abort(400, "Missing password")

    new_user = User(**data)
    new_user.save()
    return jsonify(new_user.to_dict()), 201


@app_views.route('/users/<user_id>', methods=['PUT'], strict_slashes=False)
def update_user(user_id):
    """Updates a User object"""
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    user_data = request.get_json()
    if not user_data:
        abort(400, "Not a JSON")

    ignore_keys = ['id', 'email', 'created_at', 'updated_at']
    for key, value in user_data.items():
        if key not in ignore_keys:
            setattr(user, key, value)
    user.save()
    return jsonify(user.to_dict()), 200
