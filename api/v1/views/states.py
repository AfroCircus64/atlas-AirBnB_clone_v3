#!/usr/bin/python3
""" Handles all default RESTFul API actions for the state objects """
from api.v1.views import app_views, index
from flask import Flask, abort, jsonify, request
from models import storage
from models.state import State


@app_views.route("/states", strict_slashes=False, methods=["GET"])
def list_states():
    """Method that retrieves all state objects"""
    states = storage.all(State).values()
    states_list = [state.to_dict() for state in states]
    return jsonify(states_list)


@app_views.route("/states/<state_id>", strict_slashes=False, methods=["GET"])
def get_state(state_id):
    """Method that retrieves one state object"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    return jsonify(state.to_dict())


@app_views.route(
        "/states/<state_id>", strict_slashes=False, methods=["DELETE"])
def delete_state(state_id):
    """Method that deletes a state object"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    storage.delete(state)
    storage.save()
    return jsonify({}), 200


@app_views.route("/states/<state_id>", strict_slashes=False, methods=["POST"])
def create_state():
    """Method that creates a state object"""
    data = request.get_json(silent=True)
    if not data:
        abort(400, "Not a JSON")
    if "name" not in data:
        abort(400, "Missing name")
    new_state = State(**data)
    new_state.save()
    return jsonify(new_state.to_dict()), 201


@app_views.route("/states/<state_id>", strict_slashes=False, methods=["PUT"])
def update_state(state_id):
    """Method that updates a state object"""
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    try:
        data = request.get_json()
    except Exception as e:
        abort(400, "Not a JSON")

    ignore = ['id', 'created_at', 'updated_at']
    for key, value in data.items():
        if key not in ignore:
            setattr(state, key, value)
    state.save()
    return jsonify(state.to_dict()), 200
