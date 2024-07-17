#!/usr/bin/python3
""" Handles all default RESTFul API actions for the amenity objects """
from api.v1.views import app_views
from flask import Flask, abort, jsonify, request
from models import storage
from models.amenity import Amenity


@app_views.route("/amenities", strict_slashes=False, methods=["GET"])
def list_amenities():
    """Method that retrieves all amenity objects"""
    amenity_list = []
    amenities = storage.all(Amenity).values()
    for amenity in amenities:
        amenity_list.append(amenity.to_dict())
    return jsonify(amenity_list)


@app_views.route(
    "/amenities/<amenity_id>", strict_slashes=False, methods=["GET"])
def get_amenity(amenity_id):
    """Method that retrieves one amenity object"""
    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404)
    return jsonify(amenity.to_dict())


@app_views.route(
    "/amenities/<amenity_id>", strict_slashes=False, methods=["DELETE"])
def delete_amenity(amenity_id):
    """Method that deletes an amenity object"""
    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404)
    storage.delete(amenity)
    storage.save()
    return jsonify({}), 200


@app_views.route(
    "/amenities/<amenity_id>", strict_slashes=False, methods=["POST"])
def create_amenity():
    """Method that creates an amenity object"""
    data = request.get_json(silent=True)
    if not data:
        abort(400, "Not a JSON")
    if "name" not in data:
        abort(400, "Missing name")
    amenity = Amenity(**data)
    amenity.save()
    return jsonify(amenity.to_dict())


@app_views.route(
    "/amenities/<amenity_id>", strict_slashes=False, methods=["PUT"])
def update_amenity(amenity_id):
    """Method that updates an amenity object"""
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    try:
        data = request.get_json()
    except Exception as e:
        abort(400, "Not a JSON")

    ignore = ['id', 'created_at', 'updated_at']
    for key, value in data.items():
        if key not in ignore:
            setattr(amenity, key, value)
    storage.save()
    return jsonify(amenity.to_dict()), 200
