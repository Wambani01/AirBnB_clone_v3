#!/usr/bin/python3

"""my flask file"""

from api.v1.views import app_views
from flask import Flask
from flask import jsonify
from models import storage


app = Flask(__name__)
app.register_blueprint(app_views)

@app.teardown_appcontext
def clean_up(exception=None):
    """eliminates current Session"""
    storage.close()

@app.errorhandler(404)
def not_found_error(error):
    """handles 404 error"""
    return jsonify({"error": "Not found"})

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, threaded=True)
