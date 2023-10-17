#!/usr/bin/python3
"""Amenity object view """
from flask import Flask, jsonify, request, Response
from flask import abort
from models.amenity import Amenity
from models import storage
from api.v1.views import app_views


@app_views.route("/amenities", strict_slashes=False,  methods=['GET'])
def amenitys():
    """retrieve Amenity object(s)"""
    amenity_list = []
    all_amenitys = storage.all(Amenity)
    for k, v in all_amenitys.items():
        amenity_list.append(v.to_dict())
    return jsonify(amenity_list)


@app_views.route("/amenities/<amenity_id>",
                 strict_slashes=False, methods=['GET'])
def amenity_id(amenity_id):
    """Retrieves a Amenity object based on id"""
    if amenity_id is not None:
        single_amenity = storage.get("Amenity", amenity_id)
        if single_amenity is None:
            abort(404)
        single_amenity_dict = single_amenity.to_dict()
        return jsonify(single_amenity_dict)
    else:
        abort(404)


@app_views.route("/amenities/<amenity_id>", strict_slashes=False,
                 methods=['DELETE'])
def amenity_delete(amenity_id):
    """Deletes a amenity object"""
    if amenity_id is not None:
        del_amenity = storage.get("Amenity", amenity_id)
        if del_amenity is None:
            abort(404)
        ret_del_amenity = {}
        return jsonify(ret_del_amenity)

    else:
        abort(404)


@app_views.route("/amenities", strict_slashes=False, methods=['POST'])
def amenity_add():
    """Adds a amenity object"""
    data = request.get_json()
    if data is None:
        err_return = {"error": "Not a JSON"}
        return jsonify(err_return), 400
    if "name" not in data:
        err_return = {"error": "Missing name"}
        return jsonify(err_return), 400
    new = Amenity(**data)
    storage.new(new)
    storage.save()
    status_code = 201
    new_amenity_dict = new.to_dict()
    return jsonify(new_amenity_dict), status_code


@app_views.route("/amenities/<amenity_id>",
                 strict_slashes=False, methods=['PUT'])
def amenity_update(amenity_id):
    """Update an existing amenity object"""
    data = request.get_json()
    if data is None:
        error_dict = {"error": "Not a JSON"}
        return jsonify(error_dict), 400
    single_amenity = storage.get("Amenity", amenity_id)
    if single_amenity is None:
        abort(404)

    setattr(single_amenity, 'name', data['name'])
    single_amenity.save()
    storage.save()

    return jsonify(single_amenity.to_dict())
