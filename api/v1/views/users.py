#!/usr/bin/python3

""" Handles all restful API actions for User"""

from api.v1.views import app_views
from flask import request, jsonify, abort
from models.user import User
from models import storage


@app_views.route('/users',
                 methods=['GET', 'POST'], strict_slashes=False)
@app_views.route('/users/<user_id>',
                 methods=['GET', 'PUT', 'DELETE'], strict_slashes=False)
def users(user_id=None):
    """Retrieves a list of user objects"""

    users_objs = storage.all(User)

    users = [obj.to_dict() for obj in users_objs.values()]
    if not user_id:
        if request.method == 'GET':
            return jsonify(users)
        elif request.method == 'POST':
            my_dict = request.get_json()

            if my_dict is None:
                abort(400, 'Not a JSON')
            if my_dict.get("email") is None:
                abort(400, 'Missing email')
            if my_dict.get("password") is None:
                abort(400, 'Missing password')
            new_user = User(**my_dict)
            new_user.save()
            return jsonify(new_user.to_dict()), 201
    else:
        if request.method == 'GET':
            for user in users:
                if user.get('id') == user_id:
                    return jsonify(user)
            abort(404)
        elif request.method == 'PUT':
            my_dict = request.get_json()

            if my_dict is None:
                abort(400, 'Not a JSON')
            for user in users_objs.values():
                if user.id == user_id:
                    user.name = my_dict.get("name")
                    user.save()
                    return jsonify(user.to_dict()), 200
            abort(404)

        elif request.method == 'DELETE':
            for obj in users_objs.values():
                if obj.id == user_id:
                    storage.delete(obj)
                    storage.save()
                    return jsonify({}), 200
            abort(404)
