#!/usr/bin/python3

""" Handles all restful API actions for State"""

from api.v1.views import app_views
from flask import request, jsonify, abort
from models.place import Place
from models import storage
from models.city import City


@app_views.route('cities/<city_id>/places',
                 methods=['GET', 'POST'], strict_slashes=False)
def places_by_city(city_id):
    """retrieve places based on city_id"""
    city_objs = storage.all(City)
    cities = [city for city in city_objs.values()]

    if request.method == 'GET':
        for city in cities:
            if city.id == city_id:
                places_objs = storage.all(Place)
                places = [place.to_dict()
                       for place in places_objs.values()
                       if place.city_id == city_id]
                return jsonify(places)
        abort(404)
    elif request.method == 'POST':
        for state in states:
            if state.id == state_id:
                my_dict = request.get_json()
                if my_dict is None:
                    abort(400, 'Not a JSON')
                if my_dict.get("name") is None:
                    abort(400, 'Missing name')
                my_dict["state_id"] = state_id
                city = City(**my_dict)
                city.save()
                return jsonify(city.to_dict()), 201


@app_views.route('/cities/<string:city_id>',
                 methods=['GET', 'PUT', 'DELETE'], strict_slashes=False)
def city_by_city_id(city_id):
    """retrieves cities by cities id"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    if request.method == 'GET':
        return jsonify(city.to_dict())
    elif request.method == 'DELETE':
        storage.delete(city)
        storage.save()
        return jsonify({}), 200
    elif request.method == 'PUT':
        my_dict = request.get_json()
        if my_dict is None:
            abort(400, 'Not a JSON')
        city.name = my_dict.get("name")
        city.save()
        return jsonify(city.to_dict()), 200
